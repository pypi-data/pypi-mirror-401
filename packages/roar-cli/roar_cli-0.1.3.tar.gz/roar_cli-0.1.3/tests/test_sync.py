"""Tests for roar client sync functionality."""

import time
from unittest.mock import Mock, patch

from roar.sync import SyncManager, SyncThread, get_sync_manager


class TestSyncThread:
    """Tests for SyncThread."""

    def test_sync_thread_calls_update(self):
        """Should call update_live_job on interval when I/O changes."""
        mock_client = Mock()
        mock_client.update_live_job.return_value = ({}, None)
        mock_client.heartbeat_job.return_value = ({}, None)

        # Simulate changing inputs over time
        inputs = []
        call_count = [0]

        def get_inputs():
            call_count[0] += 1
            # Add new input each call to trigger updates
            inputs.append(f"/path/file{call_count[0]}.txt")
            return inputs.copy()

        thread = SyncThread(
            job_uid="test123",
            session_hash="session456",
            laas_client=mock_client,
            get_inputs=get_inputs,
            get_outputs=lambda: [],
            sync_interval=0.1,  # Fast for testing
            heartbeat_interval=1.0,
        )

        thread.start()
        try:
            # Wait for a couple sync cycles
            time.sleep(0.35)
        finally:
            thread.stop()

        # Should have called update at least once (with changing inputs)
        assert mock_client.update_live_job.call_count >= 1

    def test_sync_thread_handles_errors(self):
        """Should continue running even if sync fails."""
        mock_client = Mock()
        mock_client.update_live_job.return_value = (None, "Network error")
        mock_client.heartbeat_job.return_value = (None, "Network error")

        thread = SyncThread(
            job_uid="test123",
            session_hash="session456",
            laas_client=mock_client,
            get_inputs=lambda: [],
            get_outputs=lambda: [],
            sync_interval=0.1,
        )

        thread.start()
        try:
            time.sleep(0.25)
            # Should still be running despite errors
            assert thread.thread.is_alive()
        finally:
            thread.stop()

    def test_sync_thread_queues_hashes(self, temp_dir):
        """Should queue files for hashing."""
        mock_client = Mock()
        mock_client.update_live_job.return_value = ({}, None)

        test_file = temp_dir / "data.txt"
        test_file.write_text("test data")

        # Need to return changing inputs to trigger updates
        files = []

        def get_inputs():
            if not files:
                files.append(str(test_file))
            return files.copy()

        thread = SyncThread(
            job_uid="test123",
            session_hash="session456",
            laas_client=mock_client,
            get_inputs=get_inputs,
            get_outputs=lambda: [],
            sync_interval=0.1,
        )

        thread.start()
        try:
            time.sleep(0.35)
        finally:
            thread.stop()

        # Verify update was called with input list
        assert mock_client.update_live_job.call_count >= 1
        call_args = mock_client.update_live_job.call_args
        inputs = call_args.kwargs.get("inputs", [])
        assert len(inputs) == 1
        assert inputs[0]["path"] == str(test_file)


class TestSyncManager:
    """Tests for SyncManager."""

    def test_initialize_disabled_by_default(self, temp_dir):
        """Should return early when sync not enabled."""
        manager = SyncManager()

        # Write a config file with sync disabled
        config_dir = temp_dir / ".roar"
        config_dir.mkdir()

        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            success, url, error = manager.initialize("session123")
        finally:
            os.chdir(old_cwd)

        assert success is True
        assert url is None
        assert error is None
        assert manager.enabled is False

    def test_initialize_registers_session(self, temp_dir):
        """Should register session with LaaS when enabled."""
        manager = SyncManager()

        mock_client = Mock()
        mock_client.register_session.return_value = (
            {"hash": "session123", "url": "http://laas/sessions/session123"},
            None,
        )

        # Create config with sync enabled
        config_dir = temp_dir / ".roar"
        config_dir.mkdir()
        config_file = config_dir / "config.toml"
        config_file.write_text("[sync]\nenabled = true\n")

        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            with (
                patch("roar.sync.get_laas_url", return_value="http://laas"),
                patch("roar.sync.LaasClient", return_value=mock_client),
            ):
                success, url, error = manager.initialize(
                    "session123",
                    git_repo="https://github.com/user/repo",
                    git_commit="abc123",
                    git_branch="main",
                )
        finally:
            os.chdir(old_cwd)

        assert success is True
        assert url == "http://laas/sessions/session123"
        assert error is None
        assert manager.enabled is True

        mock_client.register_session.assert_called_once_with(
            "session123",
            git_repo="https://github.com/user/repo",
            git_commit="abc123",
            git_branch="main",
        )

    def test_start_job_creates_live_job(self):
        """Should create live job on server."""
        manager = SyncManager()
        manager.enabled = True
        manager.session_hash = "session123"

        mock_client = Mock()
        mock_client.create_live_job.return_value = (
            {"job_uid": "job456", "status": "running"},
            None,
        )

        manager.client = mock_client

        success, error = manager.start_job(
            job_uid="job456",
            command="python train.py",
            step_number=1,
            job_type="run",
            get_inputs=lambda: [],
            get_outputs=lambda: [],
        )

        assert success is True
        assert error is None
        mock_client.create_live_job.assert_called_once()

    def test_complete_job_stops_sync_thread(self):
        """Should stop sync thread and complete job."""
        manager = SyncManager()
        manager.enabled = True
        manager.session_hash = "session123"

        mock_client = Mock()
        mock_client.complete_live_job.return_value = (
            {"job_uid": "job456", "status": "completed"},
            None,
        )
        manager.client = mock_client

        # Create a mock sync thread
        mock_thread = Mock()
        manager.sync_thread = mock_thread

        success, error = manager.complete_job(
            job_uid="job456",
            exit_code=0,
            duration_seconds=60.5,
        )

        assert success is True
        assert error is None
        mock_thread.stop.assert_called_once()
        mock_client.complete_live_job.assert_called_once()

    def test_shutdown_stops_thread(self):
        """Should stop sync thread on shutdown."""
        manager = SyncManager()
        mock_thread = Mock()
        manager.sync_thread = mock_thread

        manager.shutdown()

        mock_thread.stop.assert_called_once()
        assert manager.sync_thread is None


class TestGetSyncManager:
    """Tests for get_sync_manager singleton."""

    def test_returns_same_instance(self):
        """Should return the same manager instance."""
        import roar.sync as sync_module

        # Reset global
        sync_module._sync_manager = None

        manager1 = get_sync_manager()
        manager2 = get_sync_manager()

        assert manager1 is manager2

        # Cleanup
        sync_module._sync_manager = None
