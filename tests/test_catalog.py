import tempfile
import unittest
from pathlib import Path

from motion_asset_catalog import collect_assets, format_size


class CatalogTests(unittest.TestCase):

    def test_collects_supported_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "intro.mogrt").write_text("demo")
            (root / "notes.txt").write_text("ignore")

            assets = collect_assets(root)

            self.assertEqual(len(assets), 1)
            self.assertEqual(assets[0]["name"], "intro.mogrt")

    def test_top_level_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "main.aep").write_text("demo")
            (root / "nested").mkdir()
            (root / "nested" / "child.prproj").write_text("demo")

            assets = collect_assets(root, recursive=False)

            self.assertEqual(len(assets), 1)

    def test_format_size(self):
        self.assertEqual(format_size(512), "512 B")
        self.assertEqual(format_size(2048), "2.0 KB")


if __name__ == "__main__":
    unittest.main()
