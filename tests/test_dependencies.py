import unittest
from datetime import datetime, timezone

from ghastoolkit import Dependencies


class TestDependencies(unittest.TestCase):
    def test_export_bom_scanned_is_rfc3339_utc(self):
        before = datetime.now(timezone.utc)
        snapshot = Dependencies().exportBOM("cpdsa", "Podfile.lock")
        after = datetime.now(timezone.utc)

        self.assertRegex(
            snapshot["scanned"],
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?\+00:00$",
        )
        scanned = datetime.fromisoformat(snapshot["scanned"])
        self.assertEqual(scanned.tzinfo, timezone.utc)
        self.assertLessEqual(before, scanned)
        self.assertLessEqual(scanned, after)
