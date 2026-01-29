import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import BytesIO

from pkgstats.popcon import fetch_popcon
from pkgstats.model import PackageSummary


# ============================================================
# Unit tests (FAST, no real network)
# ============================================================


class TestDebianUnit(unittest.TestCase):

    def setUp(self):
        self.archs = ["amd64"]
        self.workdir = Path(tempfile.mkdtemp())

    # ----------------------------
    # popcon parsing
    # ----------------------------

    @patch("pkgstats.popcon.urlopen")
    def test_fetch_popcon_parses_package(self, mock_urlopen):
        fake_popcon = (
            "# comment\n"
            "1 bash 100 80 10 5 0 (Bash Maintainers)\n"
            "2 coreutils 50 40 5 3 2 (GNU Coreutils)\n"
        )

        mock_response = MagicMock()
        mock_response.__enter__.return_value = BytesIO(fake_popcon.encode())
        mock_urlopen.return_value = mock_response

        result = fetch_popcon("bash")

        self.assertIsInstance(result, PackageSummary)
        self.assertEqual(result.name, "bash")
        self.assertEqual(result.inst, 100)
        self.assertEqual(result.votes, 80)
        self.assertEqual(result.recent_installs, 5)


if __name__ == "__main__":
    unittest.main()
