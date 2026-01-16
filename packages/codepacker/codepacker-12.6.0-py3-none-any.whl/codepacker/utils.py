import os
import hashlib
from pathlib import Path

class ProjectAnalyzer:
    """
    Utility class to analyze and visualize project structures with granular exclusions.
    Designed to provide deterministic hashing for integrity checks.
    """
    
    def __init__(self, 
                 exclude_filenames=None, 
                 exclude_rel_paths=None, 
                 exclude_abs_paths=None,
                 exclude_foldernames=None,
                 exclude_folder_rel_paths=None,
                 exclude_folder_abs_paths=None,
                 exclude_extensions=None):
        """
        Initializes the analyzer with specific exclusion criteria.
        """
        # 1. File Exclusions (Standardized System Ghost Files)
        self.excl_file_names = set(exclude_filenames or {
            '.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes', 'desktop.ini', 
            '.python-version', 'META.json', 'CODE.txt'  # Added tool artifacts
        })
        self.excl_file_rel_paths = set(exclude_rel_paths or [])
        self.excl_file_abs_paths = set(exclude_abs_paths or [])

        # 2. Folder Exclusions (Standardized System/Tool Artifacts)
        self.excl_folder_names = set(exclude_foldernames or {
            '.git', '__pycache__', '.venv', 'node_modules', '.idea', '.vscode', 
            '.pytest_cache', 'env', 'venv', 'target', 'dist', 'build'
        })
        # Explicitly exclude common test/output directories to avoid "Self-Hashing"
        self.excl_folder_rel_paths = set(exclude_folder_rel_paths or {
            'bundle_output', 'working_area', 'output', 'restored_site', 'restored_project'
        })
        self.excl_folder_abs_paths = set(exclude_folder_abs_paths or [])

        # 3. Extension Exclusions
        self.excl_extensions = set(exclude_extensions or {
            '.pyc', '.pyo', '.pyd', '.tmp', '.log', '.bak', '.zip', '.tar', '.gz'
        })

    def update_exclusions(self, category, items, append=True):
        """
        Updates the exclusion lists dynamically.
        """
        attr_map = {
            'file_names': 'excl_file_names',
            'file_rel_paths': 'excl_file_rel_paths',
            'file_abs_paths': 'excl_file_abs_paths',
            'folder_names': 'excl_folder_names',
            'folder_rel_paths': 'excl_folder_rel_paths',
            'folder_abs_paths': 'excl_folder_abs_paths',
            'extensions': 'excl_extensions'
        }
        
        if category in attr_map:
            target_attr = attr_map[category]
            new_set = set(items)
            if append:
                current_set = getattr(self, target_attr)
                setattr(self, target_attr, current_set.union(new_set))
            else:
                setattr(self, target_attr, new_set)

    def _is_excluded(self, path, root_path):
        """
        Internal check to determine if a file or folder should be excluded.
        """
        path = Path(path)
        root_path = Path(root_path)
        abs_path = str(path.resolve())
        try:
            rel_path_obj = path.relative_to(root_path)
            rel_path = str(rel_path_obj)
            rel_parts = rel_path_obj.parts
        except ValueError:
            rel_path = ""
            rel_parts = []

        # Check if any part of the path (parent folders) is in an exclusion list
        for part in rel_parts:
            if part in self.excl_folder_names or part in self.excl_folder_rel_paths:
                return True

        if path.is_dir():
            if path.name in self.excl_folder_names: return True
            if rel_path in self.excl_folder_rel_paths: return True
            if abs_path in self.excl_folder_abs_paths: return True
        else:
            if path.name in self.excl_file_names: return True
            if rel_path in self.excl_file_rel_paths: return True
            if abs_path in self.excl_file_abs_paths: return True
            if path.suffix.lower() in self.excl_extensions: return True
            
        return False

    def calculate_content_hash(self, directory, debug=False):
        """
        Generates a SHA-512 hash of the directory content.
        Ensures the root directory name itself does not affect the hash.
        """
        hasher = hashlib.sha512()
        base = Path(directory).resolve()
        
        files = []
        for fp in base.rglob('*'):
            # Only hash files; directory structure is captured by relative paths
            if fp.is_file() and not self._is_excluded(fp, base):
                files.append(fp)
        
        # Sort files by POSIX relative path for absolute determinism.
        # This ensures 'restored_site/a.txt' and 'MockProject/a.txt' 
        # both use 'a.txt' as the key.
        sorted_files = sorted(files, key=lambda x: x.relative_to(base).as_posix())
        
        if debug:
            print(f"\n--- Hashing Debug for Root: {base.name} ---")

        for fp in sorted_files:
            try:
                # Force forward slashes and ensure the root name isn't part of this string
                rel_path_string = fp.relative_to(base).as_posix()
                
                if debug:
                    print(f"Hashing Path: {rel_path_string}")
                
                # Update hash with the path
                hasher.update(rel_path_string.encode('utf-8'))
                
                # Update hash with the content
                with open(fp, 'rb') as f:
                    while chunk := f.read(8192):
                        hasher.update(chunk)
            except (PermissionError, OSError) as e:
                if debug:
                    print(f"Skipping {fp}: {e}")
                continue
                
        return hasher.hexdigest()

    def build_hierarchy(self, root_path, current_path=None, indent="", is_last=True, prefix=""):
        """
        Recursively builds a visual tree string of the directory structure.
        """
        if current_path is None:
            current_path = Path(root_path)
            root_path = current_path 
        
        path = Path(current_path)
        
        if self._is_excluded(path, root_path) and prefix != "":
            return ""

        if prefix == "":
            output = f"{path.name}/\n"
        else:
            output = f"{indent}{prefix} {path.name}{'/' if path.is_dir() else ''}\n"

        if path.is_dir():
            try:
                items = [item for item in path.iterdir() if not self._is_excluded(item, root_path)]
                items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            except PermissionError:
                return f"{indent}{prefix} [Permission Denied]\n"

            for i, item in enumerate(items):
                last_item = (i == len(items) - 1)
                new_prefix = "└──" if last_item else "├──"
                new_indent = indent + ("    " if is_last else "│   ")
                pass_indent = "" if prefix == "" else new_indent
                output += self.build_hierarchy(root_path, item, pass_indent, last_item, new_prefix)
                    
        return output