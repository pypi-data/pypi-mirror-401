import os
import hashlib
import json
import uuid
import zipfile
import shutil
import io
from pathlib import Path
from collections import OrderedDict
from utils import ProjectAnalyzer

class CodePacker:
    """
    Advanced engine for consolidating code and assets with simplified Serial ID tracking.
    Enhanced with character-length guarding, per-file hashing, and ID-mapped path dictionaries.
    """
    def __init__(self, 
                 exclude_filenames=None, 
                 exclude_rel_paths=None, 
                 exclude_abs_paths=None,
                 exclude_foldernames=None,
                 exclude_folder_rel_paths=None,
                 exclude_folder_abs_paths=None,
                 exclude_extensions=None):
        
        # Initialize the ProjectAnalyzer
        self.analyzer = ProjectAnalyzer(
            exclude_filenames=exclude_filenames,
            exclude_rel_paths=exclude_rel_paths,
            exclude_abs_paths=exclude_abs_paths,
            exclude_foldernames=exclude_foldernames,
            exclude_folder_rel_paths=exclude_folder_rel_paths,
            exclude_folder_abs_paths=exclude_folder_abs_paths,
            exclude_extensions=exclude_extensions
        )
        
        self.delimiter = "#MOONSPIC_CODEPACKER#"
        self.PathOflastPack = None
        self.PathOfLastUnpack = None
        
        # Data structures for tracking
        self.code_files_registry = OrderedDict()  
        self.asset_files_registry = OrderedDict() 
        self.folder_registry = OrderedDict()      
        self.asset_folder_registry = OrderedDict() 
        
        self.last_visual_tree = ""

    def is_binary(self, file_path):
        """Check if a file is binary by looking for null bytes."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\x00' in chunk:
                    return True
                chunk.decode('utf-8')
                return False
        except (UnicodeDecodeError, PermissionError):
            return True

    def get_meta_description(self):
        """Returns a dictionary describing each key used in META.json."""
        return {
            "PROJECT_NAME": "The name of the source directory being packed.",
            "DELIMITER": "The unique string used to separate code blocks in CODE.txt.",
            "CODE_FILES_ID": "A list of unique serial IDs (F1, F2...) assigned to text-based files.",
            "FOLDER_IDS": "A list of unique serial IDs (D1, D2...) assigned to every folder.",
            "ASSET_FILES_ID": "A list of unique serial IDs assigned to binary files stored in Assets.zip.",
            "ASSET_FOLDERS_ID": "A list of IDs for folders that specifically contain asset files.",
            "ABS_PATH_TREE": "Dictionary mapping every unique ID (File/Folder) to its absolute path.",
            "REL_PATH_TREE": "Dictionary mapping every unique ID (File/Folder) to its relative path.",
            "VISUAL_TREE": "A visual ASCII representation of the project structure.",
            "CODE_ID_TO_LEN": "The exact character length of each code file for precise restoration.",
            "CODE_ID_TO_HASH": "SHA-512 hash of each individual code file for integrity verification.",
            "CONTENT_HASH": "The SHA-512 integrity hash of the project source."
        }

    def pack(self, src_path, out_dir):
        if not src_path or not out_dir: return "Error: Missing paths"
        src, out = Path(src_path).resolve(), Path(out_dir).resolve()
        
        # Reset registries and counters
        self.code_files_registry.clear()
        self.asset_files_registry.clear()
        self.folder_registry.clear()
        self.asset_folder_registry.clear()
        
        file_serial = 1
        dir_serial = 1

        # Capture visual tree and content hash
        self.last_visual_tree = self.analyzer.build_hierarchy(src)
        project_hash = self.analyzer.calculate_content_hash(src)
        
        stage = out / f"STAGE_{uuid.uuid4().hex[:6]}"
        stage.mkdir(parents=True, exist_ok=True)
        
        code_blocks = [f"{self.delimiter} PROJECT_MAP\n{self.last_visual_tree}"]
        assets_buffer = io.BytesIO()

        # Master Path Dictionaries
        abs_path_tree = {}
        rel_path_tree = {}

        with zipfile.ZipFile(assets_buffer, 'w') as az:
            for r, dirs, files in os.walk(src):
                dirs.sort()
                files.sort()
                
                curr_dir_path = Path(r)
                if self.analyzer._is_excluded(curr_dir_path, src):
                    continue

                dir_rel = str(curr_dir_path.relative_to(src))
                dir_id = f"D{dir_serial}"
                dir_serial += 1
                
                # Register directory in master path trees
                abs_path_tree[dir_id] = str(curr_dir_path)
                rel_path_tree[dir_id] = dir_rel
                self.folder_registry[dir_id] = {"abs": str(curr_dir_path), "rel": dir_rel}

                has_assets = False
                for f in files:
                    fp = Path(r) / f
                    if self.analyzer._is_excluded(fp, src): continue
                    if "_BUNDLE.zip" in f or "STAGE_" in str(fp): continue
                    
                    rel_path = str(fp.relative_to(src))
                    abs_path = str(fp.resolve())
                    
                    f_id = f"F{file_serial}"
                    file_serial += 1
                    
                    # Register file in master path trees
                    abs_path_tree[f_id] = abs_path
                    rel_path_tree[f_id] = rel_path
                    
                    if not self.is_binary(fp):
                        try:
                            content = fp.read_text(encoding='utf-8', errors='ignore')
                            c_len = len(content)
                            file_hash = hashlib.sha512(content.encode('utf-8')).hexdigest()
                            
                            def_line = f"# {self.delimiter}; {f_id}; {c_len}; {rel_path}"
                            code_blocks.append(f"{def_line}\n{content}")
                            
                            self.code_files_registry[f_id] = {
                                "abs": abs_path, 
                                "rel": rel_path, 
                                "len": c_len,
                                "hash": file_hash
                            }
                        except Exception:
                            az.write(fp, rel_path)
                            self.asset_files_registry[f_id] = {"abs": abs_path, "rel": rel_path}
                            has_assets = True
                    else:
                        az.write(fp, rel_path)
                        self.asset_files_registry[f_id] = {"abs": abs_path, "rel": rel_path}
                        has_assets = True
                
                if has_assets:
                    self.asset_folder_registry[dir_id] = self.folder_registry[dir_id]

        meta = {
            "PROJECT_NAME": src.name,
            "DELIMITER": self.delimiter,
            "CONTENT_HASH": project_hash,
            "CODE_FILES_ID": list(self.code_files_registry.keys()),
            "FOLDER_IDS": list(self.folder_registry.keys()),
            "ASSET_FILES_ID": list(self.asset_files_registry.keys()),
            "ASSET_FOLDERS_ID": list(self.asset_folder_registry.keys()),
            "ABS_PATH_TREE": abs_path_tree,
            "REL_PATH_TREE": rel_path_tree,
            "VISUAL_TREE": self.last_visual_tree,
            "CODE_ID_TO_LEN": {k: v["len"] for k, v in self.code_files_registry.items()},
            "CODE_ID_TO_HASH": {k: v["hash"] for k, v in self.code_files_registry.items()},
            "DESCRIPTION": self.get_meta_description()
        }

        (stage / "CODE.txt").write_text("\n".join(code_blocks), encoding='utf-8')
        (stage / "META.json").write_text(json.dumps(meta, indent=4), encoding='utf-8')
        (stage / "Assets.zip").write_bytes(assets_buffer.getvalue())

        final_zip = out / f"{src.name}_BUNDLE.zip"
        with zipfile.ZipFile(final_zip, 'w') as fz:
            for f in ["CODE.txt", "META.json", "Assets.zip"]:
                fz.write(stage / f, f)
        
        shutil.rmtree(stage)
        self.PathOflastPack = final_zip
        return str(final_zip)

    def unpack(self, zip_path, target_dir):
        base_target = Path(target_dir).resolve()
        temp = base_target / f"TEMP_{uuid.uuid4().hex[:6]}"
        temp.mkdir(parents=True, exist_ok=True)
        
        shutil.unpack_archive(zip_path, temp)
        meta = json.loads((temp / "META.json").read_text(encoding='utf-8'))
        
        proj_folder = base_target / meta.get("PROJECT_NAME", "restored_project")
        if proj_folder.exists(): shutil.rmtree(proj_folder)
        proj_folder.mkdir(parents=True, exist_ok=True)

        if (temp / "Assets.zip").exists():
            with zipfile.ZipFile(temp / "Assets.zip", 'r') as az:
                az.extractall(proj_folder)

        if (temp / "CODE.txt").exists():
            content = (temp / "CODE.txt").read_text(encoding='utf-8')
            delim = meta.get("DELIMITER", self.delimiter)
            
            parts = content.split(delim)
            for part in parts:
                part = part.lstrip() 
                if not part or "PROJECT_MAP" in part: continue
                
                if part.startswith(";"):
                    try:
                        header_line, remaining_body = part.split("\n", 1)
                        header_parts = [p.strip() for p in header_line.split(";")]
                        
                        expected_len = int(header_parts[2])
                        rel_path = header_parts[3]
                        
                        actual_body = remaining_body[:expected_len]
                        
                        out_f = proj_folder / rel_path
                        out_f.parent.mkdir(parents=True, exist_ok=True)
                        out_f.write_text(actual_body, encoding='utf-8')
                    except Exception:
                        continue

        shutil.rmtree(temp)
        self.PathOfLastUnpack = proj_folder
        return str(proj_folder)