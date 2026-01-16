"""Tests for roar init command."""

import subprocess


class TestRoarInit:
    """Tests for roar init command."""

    def test_init_creates_roar_dir(self, chdir_temp_git):
        result = subprocess.run(
            ["python", "-m", "roar", "init"],
            capture_output=True,
            text=True,
            input="n\n",  # Don't modify gitignore
        )
        assert result.returncode == 0
        assert (chdir_temp_git / ".roar").exists()
        assert "Created" in result.stdout

    def test_init_already_exists(self, chdir_temp_roar):
        result = subprocess.run(
            ["python", "-m", "roar", "init"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "already exists" in result.stdout

    def test_init_adds_to_gitignore(self, chdir_temp_git):
        # Ensure .gitignore exists but doesn't have .roar
        gitignore = chdir_temp_git / ".gitignore"
        gitignore.write_text("*.pyc\n")

        result = subprocess.run(
            ["python", "-m", "roar", "init"],
            capture_output=True,
            text=True,
            input="y\n",
        )
        assert result.returncode == 0
        assert "Added .roar/ to .gitignore" in result.stdout

        content = gitignore.read_text()
        assert ".roar/" in content

    def test_init_skips_gitignore_on_no(self, chdir_temp_git):
        gitignore = chdir_temp_git / ".gitignore"
        gitignore.write_text("*.pyc\n")

        result = subprocess.run(
            ["python", "-m", "roar", "init"],
            capture_output=True,
            text=True,
            input="n\n",
        )
        assert result.returncode == 0
        assert "Skipped" in result.stdout

        content = gitignore.read_text()
        assert ".roar/" not in content

    def test_init_detects_existing_gitignore_entry(self, chdir_temp_git):
        # Remove any existing .roar dir first
        roar_dir = chdir_temp_git / ".roar"
        if roar_dir.exists():
            roar_dir.rmdir()

        gitignore = chdir_temp_git / ".gitignore"
        gitignore.write_text("*.pyc\n.roar/\n")

        result = subprocess.run(
            ["python", "-m", "roar", "init"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "already in .gitignore" in result.stdout

    def test_init_outside_git_repo(self, chdir_temp):
        result = subprocess.run(
            ["python", "-m", "roar", "init"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert (chdir_temp / ".roar").exists()
        assert "Not in a git repository" in result.stdout


class TestRoarRunRequiresInit:
    """Tests that roar run requires init."""

    def test_run_without_init_fails(self, chdir_temp_git):
        result = subprocess.run(
            ["python", "-m", "roar", "run", "ls"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "roar is not initialized" in result.stdout
        assert "roar init" in result.stdout


class TestRoarConfigRequiresInit:
    """Tests that roar config requires init."""

    def test_config_without_init_fails(self, chdir_temp_git):
        result = subprocess.run(
            ["python", "-m", "roar", "config", "list"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "roar is not initialized" in result.stdout
        assert "roar init" in result.stdout

    def test_config_with_init_works(self, chdir_temp_roar):
        result = subprocess.run(
            ["python", "-m", "roar", "config", "list"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "output.track_repo_files" in result.stdout
