"""Tests for LaaS live sync functionality."""

import time

import pytest

try:
    from laas.db import LaasDB

    HAS_LAAS = True
except ImportError:
    HAS_LAAS = False
    LaasDB = None

pytestmark = pytest.mark.skipif(not HAS_LAAS, reason="laas package not installed")


class TestLaasLiveSyncDB:
    """Tests for LaasDB live sync operations."""

    @pytest.fixture
    def db(self, temp_dir):
        """Create a test LaaS database."""
        db = LaasDB(temp_dir / "laas_test.db")
        db.connect()
        yield db
        db.close()

    @pytest.fixture
    def user_id(self, db):
        """Create a test user."""
        return db.create_user(
            email="test@example.com",
            pubkey="ssh-ed25519 AAAA... test@test",
            fingerprint="SHA256:test123",
        )

    # -------------------------------------------------------------------------
    # Session tests
    # -------------------------------------------------------------------------

    def test_register_session_creates_new(self, db, user_id):
        """Should create a new session."""
        session, is_new = db.register_session(
            session_hash="abc123def456",
            user_id=user_id,
            git_repo="https://github.com/user/repo",
            git_commit="deadbeef",
            git_branch="main",
        )

        assert is_new is True
        assert session["hash"] == "abc123def456"
        assert session["git_repo"] == "https://github.com/user/repo"
        assert session["git_commit"] == "deadbeef"
        assert session["sync_enabled"] == 1
        assert session["last_activity"] is not None

    def test_register_session_updates_existing(self, db, user_id):
        """Re-registering should update last_activity."""
        session1, is_new1 = db.register_session(
            session_hash="abc123def456",
            user_id=user_id,
        )
        assert is_new1 is True
        first_activity = session1["last_activity"]

        time.sleep(0.1)

        session2, is_new2 = db.register_session(
            session_hash="abc123def456",
            user_id=user_id,
        )
        assert is_new2 is False
        assert session2["last_activity"] > first_activity

    def test_get_session_with_jobs(self, db, user_id):
        """Should get session with its jobs."""
        db.register_session("session123", user_id)
        db.create_live_job(
            job_uid="job1",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
            step_number=1,
        )
        db.create_live_job(
            job_uid="job2",
            session_hash="session123",
            user_id=user_id,
            command="python eval.py",
            step_number=2,
        )

        session = db.get_session("session123")
        assert session is not None
        assert len(session["jobs"]) == 2
        assert session["running_jobs"] == 2
        assert session["status"] == "active"

    def test_session_has_uploads(self, db, user_id):
        """Should detect when session has uploaded artifacts."""
        db.register_session("session123", user_id)

        # Initially no uploads
        session = db.get_session("session123")
        assert session["has_artifacts_uploaded"] is False

        # Create job and artifact
        job = db.create_live_job(
            job_uid="job1",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )

        # Register artifact with source_url (simulating upload)
        db.register_artifact(
            hash="artifacthash123",
            size=1000,
            user_id=user_id,
            source_type="s3",
            source_url="s3://bucket/model.pt",
        )

        # Link artifact to job
        db.conn.execute(
            "INSERT INTO job_outputs (job_id, artifact_hash) VALUES (?, ?)",
            (job["id"], "artifacthash123"),
        )
        db.conn.commit()

        session = db.get_session("session123")
        assert session["has_artifacts_uploaded"] is True

    # -------------------------------------------------------------------------
    # Live job tests
    # -------------------------------------------------------------------------

    def test_create_live_job(self, db, user_id):
        """Should create a live job."""
        db.register_session("session123", user_id)

        job = db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
            step_number=1,
            job_type="run",
        )

        assert job["job_uid"] == "job123"
        assert job["command"] == "python train.py"
        assert job["started_at"] is not None
        assert job["last_heartbeat"] is not None
        assert job["exit_code"] is None

    def test_create_live_job_idempotent(self, db, user_id):
        """Creating same job_uid twice should return existing."""
        db.register_session("session123", user_id)

        job1 = db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )
        job2 = db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )

        assert job1["id"] == job2["id"]

    def test_update_live_job(self, db, user_id):
        """Should update job with I/O state."""
        db.register_session("session123", user_id)
        db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )

        inputs = [
            {"path": "/data/train.parquet", "hash": "abc123", "size": 1000},
            {"path": "/data/val.parquet", "hash": None, "size": None},
        ]
        outputs = [
            {"path": "/checkpoints/model.pt", "hash": "def456", "size": 50000},
        ]

        job = db.update_live_job(
            job_uid="job123",
            inputs=inputs,
            outputs=outputs,
        )

        assert job is not None
        assert job["live_inputs"] is not None
        assert job["live_outputs"] is not None

        # Verify parsed I/O
        job_full = db.get_live_job("job123")
        assert len(job_full["inputs"]) == 2
        assert len(job_full["outputs"]) == 1
        assert job_full["inputs"][0]["path"] == "/data/train.parquet"

    def test_update_live_job_not_found(self, db, user_id):
        """Should return None for nonexistent job."""
        result = db.update_live_job(
            job_uid="nonexistent",
            inputs=[],
        )
        assert result is None

    def test_complete_job(self, db, user_id):
        """Should mark job as completed."""
        db.register_session("session123", user_id)
        db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )

        job = db.complete_job(
            job_uid="job123",
            exit_code=0,
            duration_seconds=3600.5,
        )

        assert job["exit_code"] == 0
        assert job["duration_seconds"] == 3600.5

        # Status should be completed
        job_full = db.get_live_job("job123")
        assert job_full["status"] == "completed"

    def test_complete_job_failed(self, db, user_id):
        """Should mark job as failed for non-zero exit."""
        db.register_session("session123", user_id)
        db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )

        db.complete_job(job_uid="job123", exit_code=1)

        job = db.get_live_job("job123")
        assert job["status"] == "failed"

    def test_heartbeat_job(self, db, user_id):
        """Should update heartbeat timestamp."""
        db.register_session("session123", user_id)
        job = db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )
        first_heartbeat = job["last_heartbeat"]

        time.sleep(0.1)

        result = db.heartbeat_job("job123")
        assert result["last_heartbeat"] > first_heartbeat

    def test_heartbeat_updates_session_activity(self, db, user_id):
        """Heartbeat should update session last_activity."""
        session, _ = db.register_session("session123", user_id)
        first_activity = session["last_activity"]

        db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )

        time.sleep(0.1)
        db.heartbeat_job("job123")

        session = db.get_session("session123")
        assert session["last_activity"] > first_activity

    def test_get_live_job_status_stale(self, db, user_id):
        """Should detect stale jobs (no heartbeat > 2 min)."""
        db.register_session("session123", user_id)
        db.create_live_job(
            job_uid="job123",
            session_hash="session123",
            user_id=user_id,
            command="python train.py",
        )

        # Manually set old heartbeat
        old_time = time.time() - 200  # 200 seconds ago
        db.conn.execute(
            "UPDATE jobs SET last_heartbeat = ? WHERE job_uid = ?", (old_time, "job123")
        )
        db.conn.commit()

        job = db.get_live_job("job123")
        assert job["status"] == "stale"

    # -------------------------------------------------------------------------
    # Dashboard tests
    # -------------------------------------------------------------------------

    def test_global_dashboard(self, db, user_id):
        """Should return global activity overview."""
        db.register_session("session1", user_id)
        db.create_live_job(
            job_uid="job1",
            session_hash="session1",
            user_id=user_id,
            command="python train.py",
        )

        dashboard = db.get_global_dashboard()
        assert dashboard["active_sessions"] >= 1
        assert dashboard["running_jobs"] >= 1
        assert len(dashboard["recent_sessions"]) >= 1

    def test_user_dashboard(self, db, user_id):
        """Should return user's sessions."""
        db.register_session("session1", user_id)
        db.register_session("session2", user_id)

        dashboard = db.get_user_dashboard(user_id)
        assert len(dashboard["sessions"]) == 2

    def test_user_dashboard_status(self, db, user_id):
        """Should correctly determine session status."""
        db.register_session("active_session", user_id)
        db.create_live_job(
            job_uid="running_job",
            session_hash="active_session",
            user_id=user_id,
            command="python train.py",
        )

        # Create inactive session
        db.register_session("inactive_session", user_id)
        # Manually set old activity
        old_time = time.time() - (2 * 86400)  # 2 days ago
        db.conn.execute(
            "UPDATE dags SET last_activity = ? WHERE hash = ?", (old_time, "inactive_session")
        )
        db.conn.commit()

        dashboard = db.get_user_dashboard(user_id)
        sessions_by_hash = {s["hash"]: s for s in dashboard["sessions"]}

        assert sessions_by_hash["active_session"]["status"] == "active"
        assert sessions_by_hash["inactive_session"]["status"] == "inactive"


class TestLaasGarbageCollection:
    """Tests for garbage collection functionality."""

    @pytest.fixture
    def db(self, temp_dir):
        """Create a test LaaS database."""
        db = LaasDB(temp_dir / "laas_test.db")
        db.connect()
        yield db
        db.close()

    @pytest.fixture
    def user_id(self, db):
        """Create a test user."""
        return db.create_user(
            email="test@example.com",
            pubkey="ssh-ed25519 AAAA... test@test",
            fingerprint="SHA256:test123",
        )

    def test_gc_stats_empty(self, db):
        """Should return zeros for empty database."""
        stats = db.get_gc_stats()
        assert stats["total_sessions"] == 0
        assert stats["total_live_jobs"] == 0
        assert stats["stale_sessions"] == 0
        assert stats["stale_jobs_with_live_data"] == 0

    def test_gc_cleans_stale_sessions(self, db, user_id):
        """Should clean sessions without uploads after 5 days."""
        # Create session and job first
        db.register_session("stale_session", user_id)
        db.create_live_job(
            job_uid="stale_job",
            session_hash="stale_session",
            user_id=user_id,
            command="python train.py",
        )
        db.update_live_job(
            job_uid="stale_job",
            inputs=[{"path": "/data/file.txt", "hash": "abc123", "size": 100}],
            outputs=[{"path": "/out/model.pt", "hash": "def456", "size": 200}],
        )

        # Now set the session to be stale (6 days old)
        # Must do this AFTER creating job since job creation updates last_activity
        old_time = time.time() - (6 * 24 * 3600)
        db.conn.execute(
            "UPDATE dags SET last_activity = ? WHERE hash = ?", (old_time, "stale_session")
        )
        db.conn.commit()

        # Verify live data exists
        job = db.get_live_job("stale_job")
        assert job["live_inputs"] is not None
        assert job["live_outputs"] is not None

        # Run GC
        result = db.gc_stale_sessions()
        assert result["sessions_cleaned"] == 1
        assert result["jobs_cleaned"] == 1

        # Verify live data is cleared
        job = db.get_live_job("stale_job")
        assert job["live_inputs"] is None
        assert job["live_outputs"] is None

    def test_gc_preserves_sessions_with_uploads(self, db, user_id):
        """Should not clean sessions that have uploaded artifacts."""
        # Create session and job
        db.register_session("uploaded_session", user_id)
        job = db.create_live_job(
            job_uid="uploaded_job",
            session_hash="uploaded_session",
            user_id=user_id,
            command="python train.py",
        )

        # Register artifact with source_url (simulating upload)
        db.register_artifact(
            hash="uploaded_artifact",
            size=1000,
            user_id=user_id,
            source_type="s3",
            source_url="s3://bucket/model.pt",
        )

        # Link artifact to job
        db.conn.execute(
            "INSERT INTO job_outputs (job_id, artifact_hash) VALUES (?, ?)",
            (job["id"], "uploaded_artifact"),
        )
        db.conn.commit()

        # Update job with live data
        db.update_live_job(
            job_uid="uploaded_job",
            inputs=[{"path": "/data/file.txt", "hash": "abc123", "size": 100}],
        )

        # Now set the session to be stale (6 days old)
        old_time = time.time() - (6 * 24 * 3600)
        db.conn.execute(
            "UPDATE dags SET last_activity = ? WHERE hash = ?", (old_time, "uploaded_session")
        )
        db.conn.commit()

        # Run GC
        result = db.gc_stale_sessions()
        assert result["sessions_cleaned"] == 0
        assert result["jobs_cleaned"] == 0

        # Verify live data is preserved
        job = db.get_live_job("uploaded_job")
        assert job["live_inputs"] is not None

    def test_gc_preserves_recent_sessions(self, db, user_id):
        """Should not clean sessions less than 5 days old."""
        # Create session and job with live data
        db.register_session("recent_session", user_id)
        db.create_live_job(
            job_uid="recent_job",
            session_hash="recent_session",
            user_id=user_id,
            command="python train.py",
        )
        db.update_live_job(
            job_uid="recent_job",
            inputs=[{"path": "/data/file.txt", "hash": "abc123", "size": 100}],
        )

        # Set session to 1 day old (still recent)
        recent_time = time.time() - (1 * 24 * 3600)
        db.conn.execute(
            "UPDATE dags SET last_activity = ? WHERE hash = ?", (recent_time, "recent_session")
        )
        db.conn.commit()

        # Run GC
        result = db.gc_stale_sessions()
        assert result["sessions_cleaned"] == 0
        assert result["jobs_cleaned"] == 0


class TestLaasLiveSyncAPI:
    """Tests for LaaS API endpoints (integration tests)."""

    @pytest.fixture
    def client(self, temp_dir):
        """Create FastAPI test client."""
        import os

        os.environ["LAAS_DB_PATH"] = str(temp_dir / "laas_test.db")

        # Need to reimport to pick up new DB path
        from fastapi.testclient import TestClient
        from laas.server import app, db

        # Reset and reconnect DB
        db.close()
        db.db_path = temp_dir / "laas_test.db"
        db.connect()

        yield TestClient(app)

        db.close()

    @pytest.fixture
    def auth_headers(self, client, temp_dir):
        """Create auth headers with a registered user."""
        # This is a simplified version - in real tests would need proper SSH signing
        # For now, skip auth testing and focus on DB layer
        pytest.skip("API tests require SSH key auth setup")

    # Note: Full API tests would require setting up SSH key auth
    # The DB tests above cover the core functionality
