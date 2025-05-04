import subprocess
import sys

def test_control_app_help():
    result = subprocess.run(
        [sys.executable, "software/control_app/control_app.py", "--help"],
        capture_output=True
    )
    assert result.returncode == 0
    out = result.stdout.decode()
    assert "Underwater" in out and "Air / altitude" in out
