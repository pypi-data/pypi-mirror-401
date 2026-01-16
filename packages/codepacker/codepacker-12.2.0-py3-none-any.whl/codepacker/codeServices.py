import os
import json
import zipfile
from pathlib import Path

class Feeder:
    """
    Responsible for segmenting the consolidated CODE.txt and providing 
    clean chunks for sequential LLM analysis.
    """
    def __init__(self, bundle_path):
        """
        Initializes the Feeder with a path to the generated BUNDLE.zip.
        """
        self.bundle_path = Path(bundle_path)
        self.segments = []
        self.meta_data = {}
        self.delimiter = "#MOONSPIC_CODEPACKER#"
        
        if self.bundle_path.exists():
            self._load_from_bundle()

    def _load_from_bundle(self):
        """
        Extracts metadata and segments the CODE.txt directly from the ZIP bundle.
        """
        try:
            with zipfile.ZipFile(self.bundle_path, 'r') as z:
                # Load Metadata
                if "META.json" in z.namelist():
                    meta_content = z.read("META.json").decode('utf-8')
                    self.meta_data = json.loads(meta_content)
                    self.delimiter = self.meta_data.get("DELIMITER", self.delimiter)

                # Load and Segment Code
                if "CODE.txt" in z.namelist():
                    code_content = z.read("CODE.txt").decode('utf-8', errors='ignore')
                    
                    # Split by the specific delimiter established in CodePacker
                    # Note: The first block is usually the PROJECT_MAP
                    raw_parts = code_content.split(self.delimiter)
                    
                    # Clean parts and re-attach the delimiter/header format for context
                    for part in raw_parts:
                        part = part.strip()
                        if not part:
                            continue
                        
                        # We re-attach the delimiter prefix so the LLM knows it's a new block
                        # The part already contains the "; ID ; Path" or "PROJECT_MAP"
                        self.segments.append(f"{self.delimiter} {part}")
                        
        except Exception as e:
            print(f"Error loading bundle for feeding: {e}")

    def get_meta_info(self):
        """Returns the metadata dictionary for external reference."""
        return self.meta_data

    def get_next_segment(self):
        """
        Generator to yield segments one by one for LLM processing.
        """
        total = len(self.segments)
        for i, segment in enumerate(self.segments):
            yield {
                "id": i + 1,
                "content": segment,
                "total": total,
                "is_map": "PROJECT_MAP" in segment
            }

    def get_segment_by_id(self, segment_id):
        """
        Retrieves a specific segment by index.
        """
        if 0 <= segment_id < len(self.segments):
            return self.segments[segment_id]
        return None