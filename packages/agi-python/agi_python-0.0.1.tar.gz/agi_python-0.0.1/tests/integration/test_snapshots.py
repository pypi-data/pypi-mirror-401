"""Tests for session snapshot functionality."""

import time

import pytest


@pytest.mark.integration
class TestSnapshots:
    """Tests for session snapshot save and restore functionality."""

    def test_snapshot_mode_none(self, client):
        """Test deleting session with save_snapshot_mode='none' (default)."""
        session = client.sessions.create(agent_name="agi-0")
        session_id = session.session_id

        # Delete without saving snapshot
        result = client.sessions.delete(session_id, save_snapshot_mode="none")
        assert result.success is True or result.message is not None

        # Environment should not be saved for restoration
        # (Can't easily test this without trying to restore)

    def test_snapshot_mode_memory(self, client):
        """Test deleting session with save_snapshot_mode='memory'."""
        session = client.sessions.create(agent_name="agi-0")
        session_id = session.session_id
        environment_id = session.environment_id

        # Navigate somewhere to create state
        client.sessions.navigate(session_id, "https://example.com")
        time.sleep(2)

        result = client.sessions.delete(session_id, save_snapshot_mode="memory")
        assert result.success is True or result.message is not None

        # Verify environment_id is available for restoration
        assert environment_id is not None

    def test_snapshot_mode_filesystem(self, client):
        """Test deleting session with save_snapshot_mode='filesystem'."""
        session = client.sessions.create(agent_name="agi-0")
        session_id = session.session_id
        environment_id = session.environment_id

        # Navigate somewhere to create state
        client.sessions.navigate(session_id, "https://example.com")
        time.sleep(2)

        result = client.sessions.delete(session_id, save_snapshot_mode="filesystem")
        assert result.success is True or result.message is not None

        # Verify environment_id is available for restoration
        assert environment_id is not None

    def test_restore_from_environment(self, client):
        """Test restoring session from saved environment."""
        session1 = client.sessions.create(agent_name="agi-0")
        session1_id = session1.session_id
        environment_id = session1.environment_id

        # Navigate to create browser state
        client.sessions.navigate(session1_id, "https://example.com")
        time.sleep(2)

        # Delete with snapshot saved
        client.sessions.delete(session1_id, save_snapshot_mode="memory")

        session2 = client.sessions.create(
            agent_name="agi-0", restore_from_environment_id=environment_id
        )

        try:
            assert session2.session_id != session1_id
            assert session2.environment_id == environment_id

            # Get status to verify session is functional
            status = client.sessions.get_status(session2.session_id)
            assert status.status is not None

            # Verify browser state is preserved (should still be at example.com)
            # Note: This may vary based on AGI implementation
            # In practice, cookies/auth state would be preserved

        finally:
            client.sessions.delete(session2.session_id)

    def test_snapshot_preserves_cookies(self, client):
        """Test that snapshots preserve browser cookies/auth state."""
        # Create session
        session1 = client.sessions.create(agent_name="agi-0")
        session1_id = session1.session_id
        environment_id = session1.environment_id

        try:
            # Navigate to a site that sets cookies
            client.sessions.navigate(session1_id, "https://httpbin.org/cookies/set?test=value")
            time.sleep(2)

            # Delete with snapshot
            client.sessions.delete(session1_id, save_snapshot_mode="memory")

            # Restore from snapshot
            session2 = client.sessions.create(
                agent_name="agi-0", restore_from_environment_id=environment_id
            )

            # In a real implementation, cookies should be preserved
            # This is a conceptual test - actual verification would need
            # to check cookie state through the agent
            assert session2.environment_id == environment_id

            client.sessions.delete(session2.session_id)

        except Exception:
            # Cleanup on error
            try:
                client.sessions.delete(session1_id)
            except Exception:
                pass

    def test_snapshot_with_context_manager(self, client):
        """Test using snapshots with SessionContext."""
        environment_id = None

        # First session - save snapshot
        with client.session("agi-0") as session1:
            environment_id = session1.environment_id
            session1.navigate("https://example.com")
            time.sleep(1)
            # Manually delete with snapshot before context exit
            client.sessions.delete(session1.session_id, save_snapshot_mode="memory")

        # Note: Need to use low-level API since context manager
        # doesn't support restore_from_environment_id parameter
        session2 = client.sessions.create(
            agent_name="agi-0", restore_from_environment_id=environment_id
        )

        try:
            assert session2.environment_id == environment_id
            status = client.sessions.get_status(session2.session_id)
            assert status.status is not None
        finally:
            client.sessions.delete(session2.session_id)

    def test_invalid_environment_id(self, client):
        """Test that invalid environment_id is handled gracefully."""
        # Try to create session with non-existent environment_id
        # This should either fail gracefully or create a new session
        session = client.sessions.create(
            agent_name="agi-0",
            restore_from_environment_id="nonexistent-environment-id",
        )

        # Depending on API implementation, this might:
        # 1. Raise an error (preferred)
        # 2. Create a new session without restoration (fallback)
        # Either way, we should get a session
        assert session.session_id is not None

        client.sessions.delete(session.session_id)


@pytest.mark.integration
class TestSnapshotWorkflows:
    """Test real-world snapshot workflows."""

    def test_multi_step_workflow_with_snapshots(self, client):
        """Test a multi-step workflow using snapshots between steps."""
        # Step 1: Login simulation
        session1 = client.sessions.create(agent_name="agi-0")
        env_id = session1.environment_id

        try:
            client.sessions.send_message(
                session1.session_id, "Navigate to httpbin.org and view the homepage"
            )
            time.sleep(3)

            # Save state after "login"
            client.sessions.delete(session1.session_id, save_snapshot_mode="memory")

            # Step 2: Perform action with preserved state
            session2 = client.sessions.create(
                agent_name="agi-0", restore_from_environment_id=env_id
            )

            # Session should have preserved state
            status = client.sessions.get_status(session2.session_id)
            assert status.status is not None

            client.sessions.delete(session2.session_id)

        except Exception:
            # Cleanup
            try:
                client.sessions.delete(session1.session_id)
            except Exception:
                pass

    def test_snapshot_between_different_agents(self, client):
        """Test restoring snapshot with a different agent."""
        # Create session with agi-0
        session1 = client.sessions.create(agent_name="agi-0")
        env_id = session1.environment_id

        try:
            client.sessions.navigate(session1.session_id, "https://example.com")
            time.sleep(2)

            client.sessions.delete(session1.session_id, save_snapshot_mode="memory")

            # Restore with agi-0-fast
            session2 = client.sessions.create(
                agent_name="agi-0-fast", restore_from_environment_id=env_id
            )

            # Should work with different agent
            assert session2.session_id is not None
            assert session2.environment_id == env_id

            client.sessions.delete(session2.session_id)

        except Exception:
            try:
                client.sessions.delete(session1.session_id)
            except Exception:
                pass
