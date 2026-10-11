import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/release_version.py"
spec = importlib.util.spec_from_file_location("release_version", SCRIPT)
release_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release_version)


class ReleaseVersionTests(unittest.TestCase):
    def test_first_release(self):
        self.assertEqual(release_version.next_version([], "minor"), (0, 1, 0))
        self.assertEqual(release_version.next_version([], "major"), (1, 0, 0))

    def test_numeric_order_and_unrelated_tags(self):
        tags = ["v1.9.0", "v1.10.3", "1.2", "backup", "v99.0.0-rc1"]
        self.assertEqual(release_version.next_version(tags, "minor"), (1, 11, 0))
        self.assertEqual(release_version.next_version(tags, "major"), (2, 0, 0))

    def test_update_preserves_other_fields_and_crlf(self):
        source = '\t"version"\t\t"3"\r\n\t"major_revision"\t\t"0"\r\n\t"minor_revision"\t\t"9"\r\n'
        expected = source.replace('"major_revision"\t\t"0"', '"major_revision"\t\t"2"').replace('"minor_revision"\t\t"9"', '"minor_revision"\t\t"0"')
        self.assertEqual(release_version.update_vdf(source, 2, 0), expected)

    def test_missing_or_duplicate_revision_rejected(self):
        for source in ('"major_revision" "0"\n', '"major_revision" "0"\n"major_revision" "1"\n"minor_revision" "0"\n'):
            with self.assertRaises(ValueError):
                release_version.update_vdf(source, 1, 0)

    def test_cli_uses_tags_and_writes_github_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            def git(*args):
                subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
            git("init")
            git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "--allow-empty", "-m", "Initial")
            git("tag", "v2.8.4")
            vdf = repo / "mapping.vdf"
            vdf.write_text('"major_revision" "0"\n"minor_revision" "0"\n')
            output = repo / "github-output"
            subprocess.run([sys.executable, str(SCRIPT), "minor", "--vdf", str(vdf), "--github-output", str(output)], cwd=repo, check=True, capture_output=True)
            self.assertEqual(output.read_text(), "tag=v2.9.0\n")
            self.assertEqual(vdf.read_text(), '"major_revision" "2"\n"minor_revision" "9"\n')


if __name__ == "__main__":
    unittest.main()
