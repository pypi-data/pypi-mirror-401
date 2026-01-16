import os
import unittest
import re
import shutil
import tempfile
from gemstone.generic_helpers import read_lines_strip_comments

class Standards:
    """Parse and query standards.txt entries."""

    def __init__(self, standards_file_path):
        self.path = standards_file_path
        self._standards = self._parse_file()

    def _parse_file(self):
        lines = read_lines_strip_comments(self.path, strip_inline_comments=False, strip_blank_lines=False)

        standards = {}
        key = None
        desc_lines = []

        def finalize_entry():
            nonlocal key, desc_lines
            if key and desc_lines:
                standards[key] = '\n'.join(desc_lines).strip()
            key, desc_lines = None, []

        for line in lines + ['']:  # sentinel blank line at end
            if not line.strip():  # blank line → end of current entry
                finalize_entry()
                continue

            candidate = re.sub(r'^[^A-Za-z0-9_]+|[^A-Za-z0-9_]+$', '', line.strip())
            if key is None and re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', candidate):
                key = candidate
                continue

            desc_lines.append(line)

        return standards

    def is_standard(self, standard_name: str) -> bool:
        """Return True if standard_name exists."""
        return standard_name in self._standards

    def get_standard_description(self, standard_name: str) -> str:
        """Return description text for given standard."""
        return self._standards.get(standard_name, "")

    def list_keys(self):
        """Return a sorted list of all standard keys."""
        return sorted(self._standards.keys())

    def __repr__(self):
        """Developer-friendly summary when printed or echoed."""
        n = len(self._standards)
        keys_preview = ', '.join(self.list_keys()[:5])
        if n > 5:
            keys_preview += ', ...'
        return f"<Standards {n} entries: {keys_preview}>"

class TestStandardsClass(unittest.TestCase):
    def setUp(self):
        self.temp_root = tempfile.mkdtemp()
        self.std_path = os.path.join(self.temp_root, "standards.txt")
        with open(self.std_path, "w") as f:
            f.write(
                "XCAT\nBinary voxelized phantom\n\n"
                "MASK\nSegmentation mask file\n\n"
            )

    def tearDown(self):
        shutil.rmtree(self.temp_root)

    def test_is_standard_true_false(self):
        s = Standards(self.std_path)
        self.assertTrue(s.is_standard("XCAT"))
        self.assertFalse(s.is_standard("Unknown"))

    def test_get_standard_description(self):
        s = Standards(self.std_path)
        desc = s.get_standard_description("MASK")
        self.assertIn("Segmentation", desc)

    def test_list_keys(self):
        s = Standards(self.std_path)
        keys = s.list_keys()
        self.assertIn("XCAT", keys)
        self.assertIn("MASK", keys)

    def test_repr_contains_keys(self):
        s = Standards(self.std_path)
        rep = repr(s)
        self.assertIn("XCAT", rep)
        self.assertIn("MASK", rep)
