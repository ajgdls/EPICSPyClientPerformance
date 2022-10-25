import subprocess
import sys

from EPICSPyClientPerformance import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "EPICSPyClientPerformance", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
