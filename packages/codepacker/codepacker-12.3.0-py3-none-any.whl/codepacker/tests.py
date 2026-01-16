import os
import shutil
import json
import zipfile
import unittest
import argparse
import sys
from pathlib import Path

# Import project components
from .utils import ProjectAnalyzer
from .codepacker import CodePacker
from .codeServices import Feeder

class TestMoonspicSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a dedicated working area for the entire test suite."""
        cls.working_area = Path("working_area").resolve()
        if cls.working_area.exists():
            shutil.rmtree(cls.working_area)
        cls.working_area.mkdir(parents=True)

    def setUp(self):
        """Set up an isolated project structure for each test case within the working area."""
        self.test_dir = self.working_area / self._testMethodName
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()

        # CRITICAL: Keep Project and Output strictly separated
        self.project_dir = self.test_dir / "SourceProject"
        self.project_dir.mkdir()
        
        (self.project_dir / "main.py").write_text("print('hello world')", encoding='utf-8')
        (self.project_dir / "utils.js").write_text("console.log('test');", encoding='utf-8')
        (self.project_dir / "README.md").write_text("# Mock Project\nThis is for testing.", encoding='utf-8')
        
        asset_dir = self.project_dir / "assets"
        asset_dir.mkdir()
        (asset_dir / "image.png").write_bytes(os.urandom(1024))
        
        self.output_dir = self.test_dir / "bundle_output"
        self.output_dir.mkdir()

    def test_analyzer_hash_consistency(self):
        """Test if the ProjectAnalyzer generates the same hash and produces output files."""
        mock_files = list(self.project_dir.rglob('*'))
        self.assertTrue(len(mock_files) > 0, "Test logic error: Mock source directory is empty.")

        packer = CodePacker()
        hash1 = packer.analyzer.calculate_content_hash(self.project_dir)
        bundle_path = packer.pack(self.project_dir, self.output_dir)
        
        output_contents = list(self.output_dir.glob('*'))
        self.assertTrue(len(output_contents) > 0, "Output directory is empty after pack operation.")
        self.assertTrue(os.path.exists(bundle_path), f"Bundle file {bundle_path} was not created.")

        hash2 = packer.analyzer.calculate_content_hash(self.project_dir)
        self.assertTrue(hash1 and len(hash1) > 0, "Analyzer returned an empty hash.")
        self.assertEqual(hash1, hash2, "Deterministic hashing failed: hashes should be identical.")

    def test_packer_meta_format(self):
        """Verify that META.json uses all CAPS keys and includes the descriptive dictionary."""
        packer = CodePacker()
        bundle_path = Path(packer.pack(self.project_dir, self.output_dir))
        
        with zipfile.ZipFile(bundle_path, 'r') as z:
            meta_content = z.read("META.json").decode('utf-8')
            meta_data = json.loads(meta_content)
            
            required_keys = [
                "PROJECT_NAME", "DELIMITER", "CODE_FILES_ID", 
                "FOLDER_IDS", "CONTENT_HASH", "DESCRIPTION"
            ]
            for key in required_keys:
                self.assertIn(key, meta_data, f"Missing required CAPS key: {key}")
            
            self.assertIsInstance(meta_data["DESCRIPTION"], dict)

    def test_packer_header_format(self):
            """Verify the definition line format in CODE.txt matches the specification."""
            packer = CodePacker()
            bundle_path = Path(packer.pack(self.project_dir, self.output_dir))
            
            with zipfile.ZipFile(bundle_path, 'r') as z:
                code_text = z.read("CODE.txt").decode('utf-8')
                # Updated expectation: Look for the delimiter followed by the new Serial ID prefix 'F'
                # Instead of 'CODE_', we now use 'F1', 'F2', etc.
                expected_prefix = f"# {packer.delimiter}; F" 
                self.assertIn(expected_prefix, code_text, "CODE.txt does not contain correctly formatted header lines.")

    def test_integrity_match(self):
        """Test the full cycle: Pack -> Unpack -> Compare Hashes."""
        packer = CodePacker()
        
        # 1. Calculate Original Hash
        h1 = packer.analyzer.calculate_content_hash(self.project_dir)
        
        # 2. Pack to bundle_output/
        bundle = packer.pack(self.project_dir, self.output_dir)
        
        # 3. Unpack to restored_site/
        restoration_path = self.test_dir / "restored_site"
        restoration_path.mkdir()
        restored_dir = packer.unpack(bundle, restoration_path)
        
        # 4. Calculate Restored Hash
        h2 = packer.analyzer.calculate_content_hash(restored_dir)
        
        # Debugging info if it fails
        if h1 != h2:
            print("\n--- Integrity Debug ---")
            print(f"Original Dir: {self.project_dir}")
            print(f"Restored Dir: {restored_dir}")
            orig_files = sorted([str(p.relative_to(self.project_dir)) for p in self.project_dir.rglob('*')])
            rest_files = sorted([str(p.relative_to(restored_dir)) for p in Path(restored_dir).rglob('*')])
            print(f"Original Files: {len(orig_files)}")
            print(f"Restored Files: {len(rest_files)}")
            if orig_files != rest_files:
                print(f"File list mismatch! Missing/Extra: {set(orig_files) ^ set(rest_files)}")
        
        self.assertEqual(h1, h2, "Integrity Mismatch: The restored project content has been altered.")

    def test_feeder_segmentation(self):
        """Verify the Feeder correctly parses the bundle and yields project segments."""
        packer = CodePacker()
        bundle = packer.pack(self.project_dir, self.output_dir)
        
        feeder = Feeder(bundle)
        segments = list(feeder.get_next_segment())
        
        self.assertEqual(len(segments), 4, f"Expected 4 segments, found {len(segments)}")
        self.assertTrue(segments[0]["is_map"], "The first segment yielded should be the PROJECT_MAP.")

def list_tests(suite):
    test_methods = []
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            test_methods.extend(list_tests(test))
        else:
            test_methods.append(test._testMethodName)
    return test_methods

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moonspic System Test Runner")
    parser.add_argument("-n", "--number", type=int, help="Run a specific test by its index number")
    parser.add_argument("-l", "--list", action="store_true", help="List all available tests with their index numbers")
    
    args = parser.parse_args()

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMoonspicSystem)
    all_test_names = list_tests(suite)

    if args.list:
        print("\nAvailable Tests:")
        for idx, name in enumerate(all_test_names, 1):
            print(f" [{idx}] {name}")
        sys.exit(0)

    if args.number is not None:
        if 1 <= args.number <= len(all_test_names):
            test_name = all_test_names[args.number - 1]
            specific_suite = loader.loadTestsFromName(f"{__name__}.TestMoonspicSystem.{test_name}")
            unittest.TextTestRunner(verbosity=2).run(specific_suite)
        else:
            print(f"❌ Error: Invalid test number.")
            sys.exit(1)
    else:
        unittest.TextTestRunner(verbosity=2).run(suite)