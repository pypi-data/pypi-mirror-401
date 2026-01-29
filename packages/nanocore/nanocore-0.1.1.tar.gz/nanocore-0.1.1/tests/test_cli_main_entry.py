"""
Final coverage tests for cli.py to reach 100%.
Tests the __main__ entry point execution.
"""

import sys
import subprocess
import pytest


def test_cli_main_execution():
    """Test executing cli.py as a script directly."""
    # This tests the if __name__ == "__main__": main() block
    # by running the module as a script
    result = subprocess.run(
        [sys.executable, "-m", "nanocore.cli", "--help"],
        capture_output=True,
        text=True,
        timeout=5,
    )

    # Should exit successfully and show help
    assert result.returncode == 0
    assert "connect" in result.stdout.lower() or "connect" in result.stderr.lower()


def test_connect_keyboard_interrupt_direct():
    """Test that KeyboardInterrupt in connect is handled gracefully."""
    from unittest.mock import patch
    from nanocore.cli import connect

    # Patch asyncio.run to raise KeyboardInterrupt
    with patch("nanocore.cli.asyncio.run", side_effect=KeyboardInterrupt):
        # This should not raise an exception
        try:
            connect(url="ws://localhost:8000/ws")
            # If we get here, the KeyboardInterrupt was caught
            assert True
        except KeyboardInterrupt:
            # Should not propagate
            pytest.fail("KeyboardInterrupt should have been caught")
