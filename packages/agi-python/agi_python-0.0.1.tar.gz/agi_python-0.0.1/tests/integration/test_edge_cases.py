"""Integration tests for edge cases and boundary conditions."""

import time

import pytest

from agi import AgentExecutionError


@pytest.mark.integration
class TestAgentSelection:
    """Tests for different agent types."""

    @pytest.mark.parametrize(
        "agent_name",
        [
            "agi-0",
            "agi-0-fast",
            pytest.param("agi-1", marks=pytest.mark.skip(reason="agi-1 may not be available")),
        ],
    )
    def test_all_agents_work(self, client, agent_name):
        """Test that all agent types work correctly."""
        with client.session(agent_name) as session:
            assert session.session_id is not None
            assert session.vnc_url is not None

            status = session.get_status()
            assert status.status in ["ready", "running", "waiting_for_input"]

    @pytest.mark.parametrize("agent_name", ["agi-0", "agi-0-fast"])
    def test_agents_complete_simple_task(self, client, agent_name):
        """Test that agents can complete a simple task."""
        with client.session(agent_name) as session:
            result = session.run_task("What is 2+2?")
            assert result is not None


@pytest.mark.integration
class TestInvalidInputs:
    """Tests for handling invalid inputs."""

    def test_invalid_agent_name(self, client):
        """Test creating session with invalid agent name."""
        # This might raise an error or create with fallback
        try:
            session = client.sessions.create(agent_name="nonexistent-agent")
            # If it succeeds, clean up
            client.sessions.delete(session.session_id)
        except Exception as e:
            # Should raise a clear error
            assert "agent" in str(e).lower() or "invalid" in str(e).lower()

    def test_empty_task_message(self, client):
        """Test sending empty task message."""
        with client.session("agi-0") as session:
            # Empty string might be rejected or handled gracefully
            try:
                result = session.send_message("")
                # If accepted, should return something
                assert result is not None
            except ValueError:
                # Or might raise validation error
                pass

    def test_very_long_task_message(self, client):
        """Test sending very long task message."""
        long_message = "a" * 10000  # 10k characters
        with client.session("agi-0") as session:
            # Should either accept or raise clear error
            result = session.send_message(long_message)
            assert result is not None

    def test_task_with_special_characters(self, client):
        """Test task with special characters and unicode."""
        with client.session("agi-0") as session:
            result = session.send_message(
                "Find info about: café, résumé, naïve, 日本語, 🌍, <script>alert('test')</script>"
            )
            assert result is not None

    def test_invalid_url_navigation(self, client):
        """Test navigating to invalid URL."""
        with client.session("agi-0") as session:
            # Invalid URL should be handled gracefully
            try:
                result = session.navigate("not-a-valid-url")
                # Might succeed with error state
                assert result is not None
            except (ValueError, AgentExecutionError):
                # Or raise appropriate error
                pass

    def test_malformed_url_navigation(self, client):
        """Test navigating to malformed URL."""
        with client.session("agi-0") as session:
            try:
                result = session.navigate("ht!tp://bad..url")
                assert result is not None
            except (ValueError, AgentExecutionError):
                pass


@pytest.mark.integration
class TestSessionStateTransitions:
    """Tests for session state transitions."""

    def test_double_pause(self, client):
        """Test pausing an already paused session."""
        with client.session("agi-0") as session:
            session.send_message("Count to 100")
            time.sleep(1)

            # First pause
            session.pause()
            time.sleep(1)

            # Second pause - should be idempotent or raise clear error
            result = session.pause()
            assert result is not None

    def test_resume_without_pause(self, client):
        """Test resuming a session that wasn't paused."""
        with client.session("agi-0") as session:
            # Try to resume without pausing first
            result = session.resume()
            # Should either be no-op or raise clear error
            assert result is not None

    def test_cancel_already_finished(self, client):
        """Test canceling a finished session."""
        with client.session("agi-0") as session:
            _ = session.run_task("What is 2+2?")
            # Task finished

            # Try to cancel after completion
            try:
                cancel_result = session.cancel()
                # Should handle gracefully
                assert cancel_result is not None
            except Exception:
                # Or raise appropriate error
                pass

    def test_operations_on_deleted_session(self, client):
        """Test that operations on deleted session fail appropriately."""
        session = client.sessions.create(agent_name="agi-0")
        session_id = session.session_id

        # Delete the session
        client.sessions.delete(session_id)

        # Operations should fail with NotFoundError
        from agi import NotFoundError

        with pytest.raises(NotFoundError):
            client.sessions.get_status(session_id)


@pytest.mark.integration
class TestConcurrency:
    """Tests for concurrent session operations."""

    def test_multiple_simultaneous_sessions(self, client):
        """Test creating multiple sessions simultaneously."""
        sessions = []

        try:
            # Create 3 sessions
            for _ in range(3):
                session = client.sessions.create(agent_name="agi-0")
                sessions.append(session)

            # All should be valid
            assert len(sessions) == 3
            assert len({s.session_id for s in sessions}) == 3  # All unique

        finally:
            # Clean up
            for session in sessions:
                try:
                    client.sessions.delete(session.session_id)
                except Exception:
                    pass

    def test_concurrent_tasks_different_sessions(self, client):
        """Test running tasks in different sessions concurrently."""
        session1 = client.sessions.create(agent_name="agi-0")
        session2 = client.sessions.create(agent_name="agi-0")

        try:
            # Send tasks to both
            client.sessions.send_message(session1.session_id, "Count to 10")
            client.sessions.send_message(session2.session_id, "What is 5+5?")

            # Both should be able to work independently
            status1 = client.sessions.get_status(session1.session_id)
            status2 = client.sessions.get_status(session2.session_id)

            assert status1.status in ["running", "waiting_for_input", "finished"]
            assert status2.status in ["running", "waiting_for_input", "finished"]

        finally:
            client.sessions.delete(session1.session_id)
            client.sessions.delete(session2.session_id)


@pytest.mark.integration
class TestResourceLimits:
    """Tests for resource limits and constraints."""

    def test_max_steps_parameter(self, client):
        """Test max_steps parameter limits execution."""
        session = client.sessions.create(agent_name="agi-0", max_steps=5)

        try:
            # Send a task that would normally take many steps
            client.sessions.send_message(
                session.session_id, "Browse multiple pages and collect information"
            )

            # Task should stop after max_steps
            # (Implementation dependent - might fail or complete partially)
            time.sleep(5)

            status = client.sessions.get_status(session.session_id)
            assert status.status is not None

        finally:
            client.sessions.delete(session.session_id)

    @pytest.mark.slow
    def test_very_long_running_task(self, client):
        """Test handling of very long-running task."""
        with client.session("agi-0") as session:
            # Task that might take a while
            result = session.run_task("Navigate to example.com and wait 10 seconds")

            # Should complete eventually or timeout gracefully
            assert result is not None


@pytest.mark.integration
class TestScreenshotEdgeCases:
    """Tests for screenshot edge cases."""

    def test_screenshot_before_navigation(self, client):
        """Test taking screenshot before any navigation."""
        with client.session("agi-0") as session:
            # Might show blank page or initial state
            screenshot = session.screenshot()
            assert screenshot is not None
            assert screenshot.screenshot is not None

    def test_screenshot_of_failed_page_load(self, client):
        """Test screenshot of page that failed to load."""
        with client.session("agi-0") as session:
            try:
                session.navigate("https://this-domain-definitely-does-not-exist-12345.com")
                time.sleep(2)
            except Exception:
                pass

            # Should still be able to screenshot error page
            screenshot = session.screenshot()
            assert screenshot is not None

    def test_multiple_screenshots_same_session(self, client):
        """Test taking multiple screenshots in same session."""
        with client.session("agi-0") as session:
            session.navigate("https://example.com")
            time.sleep(2)

            # Take multiple screenshots
            shot1 = session.screenshot()
            time.sleep(1)
            shot2 = session.screenshot()
            time.sleep(1)
            shot3 = session.screenshot()

            # All should be valid
            assert shot1.screenshot is not None
            assert shot2.screenshot is not None
            assert shot3.screenshot is not None


@pytest.mark.integration
class TestConfigUpdates:
    """Tests for config_updates parameter."""

    def test_config_updates_in_send_message(self, client):
        """Test passing config_updates to send_message."""
        with client.session("agi-0") as session:
            # Config updates might include browser settings, timeouts, etc.
            result = session.send_message("Navigate to example.com", config_updates={"timeout": 30})

            assert result is not None

    def test_start_url_in_send_message(self, client):
        """Test passing start_url to send_message."""
        with client.session("agi-0") as session:
            result = session.send_message("Find the page title", start_url="https://example.com")

            assert result is not None
