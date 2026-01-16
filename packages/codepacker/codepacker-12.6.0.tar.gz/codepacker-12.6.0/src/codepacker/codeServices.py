import os
import json
import zipfile
import hashlib
from pathlib import Path

class Feeder:
    """
    Responsible for segmenting the consolidated CODE.txt and providing 
    clean chunks for sequential LLM analysis or Agentic retrieval.
    Enhanced to support Serial ID indexing and integrity verification.
    """
    def __init__(self, bundle_path):
        """
        Initializes the Feeder with a path to the generated BUNDLE.zip.
        """
        self.bundle_path = Path(bundle_path)
        self.segments = [] # Sequential list for iteration
        self.id_map = {}   # Map for direct ID access (F1, F2...)
        self.stream_segments = [] # Array of dictionaries: {'code', 'fileID', 'relativepath'}
        self.meta_data = {}
        self.delimiter = "#MOONSPIC_CODEPACKER#"
        
        if self.bundle_path.exists():
            self._load_from_bundle()

    def _load_from_bundle(self):
        """
        Extracts metadata and segments the CODE.txt directly from the ZIP bundle.
        Uses line-by-line parsing to populate stream_segments.
        """
        try:
            with zipfile.ZipFile(self.bundle_path, 'r') as z:
                # 1. Load Metadata
                if "META.json" in z.namelist():
                    meta_content = z.read("META.json").decode('utf-8')
                    self.meta_data = json.loads(meta_content)
                    self.delimiter = self.meta_data.get("DELIMITER", self.delimiter)

                # 2. Load and Segment Code
                if "CODE.txt" in z.namelist():
                    code_content = z.read("CODE.txt").decode('utf-8', errors='ignore')
                    lines = code_content.splitlines()
                    
                    current_header = None
                    current_code_lines = []

                    def save_current_block():
                        if not current_header:
                            return
                        
                        code_string = "\n".join(current_code_lines).strip()
                        
                        # Handle MAP or File blocks
                        if "PROJECT_MAP" in current_header:
                            f_id = "MAP"
                            rel_path = "PROJECT_MAP"
                        else:
                            # Parse: "# DELIMITER; ID; Length; Path"
                            parts = [p.strip() for p in current_header.split(";")]
                            f_id = parts[1] if len(parts) > 1 else "UNKNOWN"
                            rel_path = parts[3] if len(parts) > 3 else "UNKNOWN"

                        segment_dict = {
                            'code': code_string,
                            'fileID': f_id,
                            'relativepath': rel_path
                        }
                        
                        self.stream_segments.append(segment_dict)
                        # Maintain legacy structures for backward compatibility
                        full_segment = f"{current_header}\n{code_string}"
                        self.segments.append(full_segment)
                        self.id_map[f_id] = full_segment

                    for line in lines:
                        if line.startswith(self.delimiter) or line.startswith(f"# {self.delimiter}"):
                            # Before starting a new block, save the previous one
                            save_current_block()
                            # Reset for the new block
                            current_header = line
                            current_code_lines = []
                        else:
                            if current_header:
                                current_code_lines.append(line)
                    
                    # Save the final block in the file
                    save_current_block()
                                        
        except Exception as e:
            print(f"Error loading bundle for feeding: {e}")

    def verify_segment_integrity(self, serial_id):
        """
        Checks if the segment in memory matches the SHA-512 and length 
        stored in the bundle's META.json.
        """
        if serial_id not in self.id_map:
            return False, "ID not found"
        
        segment = self.id_map[serial_id]
        meta_hashes = self.meta_data.get("CODE_ID_TO_HASH", {})
        meta_lengths = self.meta_data.get("CODE_ID_TO_LEN", {})
        
        # Extract actual body content (skipping header line)
        try:
            body_content = segment.split("\n", 1)[1]
            actual_len = len(body_content)
            actual_hash = hashlib.sha512(body_content.encode('utf-8')).hexdigest()
            
            expected_len = meta_lengths.get(serial_id)
            expected_hash = meta_hashes.get(serial_id)
            
            if actual_len == expected_len and actual_hash == expected_hash:
                return True, "Integrity Verified"
            else:
                return False, f"Mismatch: Len({actual_len}/{expected_len}) Hash Match: {actual_hash == expected_hash}"
        except Exception as e:
            return False, str(e)

    def get_meta_info(self):
        """Returns the metadata dictionary for external reference."""
        return self.meta_data

    def get_next_segment(self):
        """
        Generator to yield segments one by one for sequential LLM processing.
        """
        total = len(self.segments)
        for i, segment in enumerate(self.segments):
            # Attempt to extract ID for metadata reporting
            current_id = "UNKNOWN"
            if "PROJECT_MAP" in segment:
                current_id = "MAP"
            elif ";" in segment:
                try:
                    current_id = segment.split(";")[1].strip()
                except: pass

            yield {
                "index": i,
                "serial_id": current_id,
                "content": segment,
                "total": total,
                "is_map": "PROJECT_MAP" in segment
            }

    def get_segment_by_serial(self, serial_id):
        """
        Retrieves a specific segment by its Serial ID (e.g., 'F1', 'D5', 'MAP').
        Essential for Agentic AI looking for specific file context.
        """
        return self.id_map.get(serial_id)