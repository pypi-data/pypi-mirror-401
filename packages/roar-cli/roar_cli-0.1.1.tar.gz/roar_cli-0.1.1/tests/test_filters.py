"""Tests for roar filters module."""

import os
from pathlib import Path

from roar.filters.files import FileClassifier


class TestFileClassifier:
    """Tests for FileClassifier."""

    def test_classify_nonexistent_file(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        result, pkg = classifier.classify("/nonexistent/path/file.txt")
        assert result == "skip"
        assert pkg is None

    def test_classify_dev_null(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        result, pkg = classifier.classify("/dev/null")
        assert result == "external"
        assert pkg is None

    def test_classify_proc_file(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        result, pkg = classifier.classify("/proc/self/maps")
        assert result == "external"
        assert pkg is None

    def test_classify_tracked_repo_file(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        readme = temp_git_repo / "README.md"
        result, pkg = classifier.classify(str(readme))
        assert result == "repo"
        assert pkg is None

    def test_classify_untracked_repo_file(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        # Create file but don't git add
        untracked = temp_git_repo / "untracked.txt"
        untracked.write_text("test")

        result, pkg = classifier.classify(str(untracked))
        assert result == "unmanaged"
        assert pkg is None

    def test_classify_system_lib(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        # libc should exist on Linux
        libc = "/usr/lib/x86_64-linux-gnu/libc.so.6"
        if os.path.exists(libc):
            result, _pkg = classifier.classify(libc)
            assert result == "system"

    def test_classify_etc_file(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        passwd = "/etc/passwd"
        if os.path.exists(passwd):
            result, _pkg = classifier.classify(passwd)
            assert result == "system"

    def test_classify_stdlib_file(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        # os.py should be in stdlib
        import os as os_module

        os_path = os_module.__file__
        if os_path:
            result, _pkg = classifier.classify(os_path)
            assert result == "stdlib"

    def test_classify_skips_roar_inject_dir(self, temp_git_repo):
        inject_dir = str(temp_git_repo / "inject")
        os.makedirs(inject_dir, exist_ok=True)
        test_file = Path(inject_dir) / "sitecustomize.py"
        test_file.write_text("# test")

        classifier = FileClassifier(repo_root=str(temp_git_repo), roar_inject_dir=inject_dir)
        result, _pkg = classifier.classify(str(test_file))
        assert result == "skip"


class TestFileClassifierClassifyAll:
    """Tests for FileClassifier.classify_all."""

    def test_classify_all_empty_list(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        result = classifier.classify_all([])
        assert result["repo_files"] == []
        assert result["packages"] == {}
        assert result["unmanaged"] == []

    def test_classify_all_mixed_files(self, temp_git_repo):
        # Create an untracked file
        untracked = temp_git_repo / "untracked.txt"
        untracked.write_text("test")

        readme = temp_git_repo / "README.md"

        classifier = FileClassifier(repo_root=str(temp_git_repo))
        result = classifier.classify_all(
            [
                str(readme),
                str(untracked),
                "/dev/null",
                "/nonexistent",
            ]
        )

        assert str(readme) in result["repo_files"]
        assert str(untracked) in result["unmanaged"]
        # /dev/null and /nonexistent should not appear in any list

    def test_classify_all_stats(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        readme = temp_git_repo / "README.md"

        result = classifier.classify_all(
            [
                str(readme),
                "/dev/null",
                "/nonexistent",
            ]
        )

        assert result["stats"]["repo"] == 1
        assert result["stats"]["external"] == 1
        assert result["stats"]["skip"] == 1

    def test_classify_all_skips_empty_strings(self, temp_git_repo):
        classifier = FileClassifier(repo_root=str(temp_git_repo))
        result = classifier.classify_all(["", None, ""])
        # Should not crash, empty results
        assert result["repo_files"] == []


class TestFileClassifierVenv:
    """Tests for venv/site-packages handling."""

    def test_classify_venv_file_as_package(self, temp_git_repo):
        # Create a fake venv structure
        venv = temp_git_repo / ".venv"
        site_packages = venv / "lib" / "python3.10" / "site-packages"
        site_packages.mkdir(parents=True)
        pkg_file = site_packages / "somepkg" / "__init__.py"
        pkg_file.parent.mkdir()
        pkg_file.write_text("")

        classifier = FileClassifier(repo_root=str(temp_git_repo), sys_prefix=str(venv))
        result, _pkg = classifier.classify(str(pkg_file))
        # Should be classified as package (even if unknown)
        assert result == "package"
