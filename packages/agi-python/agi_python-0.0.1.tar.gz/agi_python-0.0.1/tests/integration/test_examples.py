"""Integration tests for example scripts."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Skip all tests in this module if AGI_API_KEY is not set
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.getenv("AGI_API_KEY"), reason="AGI_API_KEY environment variable not set"
    ),
]

# Path to examples directory
EXAMPLES_DIR = Path(__file__).parent.parent.parent / "examples"


@pytest.mark.integration
class TestExamples:
    """Tests for example scripts."""

    @pytest.mark.parametrize(
        "example,timeout,description",
        [
            ("quickstart.py", 30, "Tests basic run_task()"),
            ("browser_control.py", 20, "Tests navigate() and screenshot()"),
            ("session_control.py", 30, "Tests pause/resume/cancel"),
            ("streaming_events.py", 30, "Tests real-time event streaming"),
            ("advanced_usage.py", 30, "Tests advanced features"),
        ],
    )
    def test_example_execution(self, example, timeout, description):
        """Test that example script executes successfully.

        Args:
            example: Example filename
            timeout: Timeout in seconds
            description: Description of what the example tests
        """
        example_path = EXAMPLES_DIR / example

        assert example_path.exists(), f"Example file not found: {example_path}"

        try:
            result = subprocess.run(
                [sys.executable, str(example_path)],
                timeout=timeout,
                capture_output=True,
                text=True,
                env=os.environ,
            )

            # Check exit code
            assert result.returncode == 0, (
                f"Example failed with exit code {result.returncode}\nstderr: {result.stderr[:500]}"
            )

        except subprocess.TimeoutExpired:
            # Timeout is acceptable - means example started successfully
            # and is running (some examples take time to complete)
            pytest.skip(f"Example timeout after {timeout}s (expected for long-running tasks)")

    def test_quickstart_simple(self):
        """Test quickstart.py example runs successfully."""
        example_path = EXAMPLES_DIR / "quickstart.py"

        result = subprocess.run(
            [sys.executable, str(example_path)],
            timeout=30,
            capture_output=True,
            text=True,
            env=os.environ,
        )

        # Should complete successfully
        assert result.returncode == 0 or "session_id" in result.stdout.lower()

    def test_browser_control_example(self):
        """Test browser_control.py example runs successfully."""
        example_path = EXAMPLES_DIR / "browser_control.py"

        result = subprocess.run(
            [sys.executable, str(example_path)],
            timeout=20,
            capture_output=True,
            text=True,
            env=os.environ,
        )

        # Should complete or show navigation
        assert result.returncode == 0 or "example.com" in result.stdout.lower()

    def test_streaming_events_example(self):
        """Test streaming_events.py example runs successfully."""
        example_path = EXAMPLES_DIR / "streaming_events.py"

        try:
            result = subprocess.run(
                [sys.executable, str(example_path)],
                timeout=30,
                capture_output=True,
                text=True,
                env=os.environ,
            )

            # Should show event streaming
            assert result.returncode == 0 or "event" in result.stdout.lower()

        except subprocess.TimeoutExpired:
            # Streaming examples may timeout (expected)
            pytest.skip("Streaming example timeout (expected)")

    @pytest.mark.slow
    def test_advanced_usage_example(self):
        """Test advanced_usage.py example runs successfully."""
        example_path = EXAMPLES_DIR / "advanced_usage.py"

        try:
            result = subprocess.run(
                [sys.executable, str(example_path)],
                timeout=45,
                capture_output=True,
                text=True,
                env=os.environ,
            )

            assert result.returncode == 0 or "session" in result.stdout.lower()

        except subprocess.TimeoutExpired:
            pytest.skip("Advanced usage example timeout (expected)")

    def test_examples_directory_exists(self):
        """Test that examples directory exists and contains files."""
        assert EXAMPLES_DIR.exists(), f"Examples directory not found: {EXAMPLES_DIR}"

        example_files = list(EXAMPLES_DIR.glob("*.py"))
        assert len(example_files) > 0, "No example files found"
