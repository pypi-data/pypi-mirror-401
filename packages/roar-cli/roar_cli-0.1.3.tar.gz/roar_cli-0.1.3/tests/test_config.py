"""Tests for roar config module."""

import pytest

from roar.config import (
    CONFIGURABLE_KEYS,
    DEFAULT_CONFIG,
    _get_nested,
    _set_nested,
    config_get,
    config_set,
    find_config_file,
    get_roar_dir,
    load_config,
    save_config,
)


class TestNestedHelpers:
    """Tests for nested dict helpers."""

    def test_get_nested_simple(self):
        d = {"a": {"b": {"c": 1}}}
        assert _get_nested(d, "a.b.c") == 1

    def test_get_nested_missing(self):
        d = {"a": {"b": 1}}
        assert _get_nested(d, "a.b.c") is None
        assert _get_nested(d, "a.b.c", "default") == "default"

    def test_get_nested_top_level(self):
        d = {"a": 1}
        assert _get_nested(d, "a") == 1

    def test_set_nested_simple(self):
        d = {}
        _set_nested(d, "a.b.c", 1)
        assert d == {"a": {"b": {"c": 1}}}

    def test_set_nested_existing(self):
        d = {"a": {"b": {"c": 1}}}
        _set_nested(d, "a.b.c", 2)
        assert d["a"]["b"]["c"] == 2

    def test_set_nested_top_level(self):
        d = {}
        _set_nested(d, "a", 1)
        assert d == {"a": 1}


class TestDefaultConfig:
    """Tests for default configuration."""

    def test_default_config_has_output(self):
        assert "output" in DEFAULT_CONFIG
        assert "track_repo_files" in DEFAULT_CONFIG["output"]
        assert DEFAULT_CONFIG["output"]["track_repo_files"] is False

    def test_default_config_has_analyzers(self):
        assert "analyzers" in DEFAULT_CONFIG
        assert "experiment_tracking" in DEFAULT_CONFIG["analyzers"]
        assert DEFAULT_CONFIG["analyzers"]["experiment_tracking"] is True

    def test_default_config_has_filters(self):
        assert "filters" in DEFAULT_CONFIG
        assert "ignore_system_reads" in DEFAULT_CONFIG["filters"]
        assert "ignore_package_reads" in DEFAULT_CONFIG["filters"]
        assert "ignore_torch_cache" in DEFAULT_CONFIG["filters"]
        assert DEFAULT_CONFIG["filters"]["ignore_system_reads"] is True
        assert DEFAULT_CONFIG["filters"]["ignore_package_reads"] is True
        assert DEFAULT_CONFIG["filters"]["ignore_torch_cache"] is True

    def test_configurable_keys_match_defaults(self):
        """All configurable keys should exist in defaults."""
        for key in CONFIGURABLE_KEYS:
            value = _get_nested(DEFAULT_CONFIG, key)
            assert value is not None or value == CONFIGURABLE_KEYS[key]["default"]


class TestLoadConfig:
    """Tests for config loading."""

    def test_load_config_no_file_returns_defaults(self, temp_dir):
        config = load_config(start_dir=str(temp_dir))
        assert config["output"]["track_repo_files"] is False
        assert config["analyzers"]["experiment_tracking"] is True

    def test_load_config_from_file(self, temp_dir):
        # Create .roar/config.toml
        roar_dir = temp_dir / ".roar"
        roar_dir.mkdir()
        config_file = roar_dir / "config.toml"
        config_file.write_text("[output]\ntrack_repo_files = true\n")

        config = load_config(start_dir=str(temp_dir))
        assert config["output"]["track_repo_files"] is True
        # Other defaults should still be present
        assert config["analyzers"]["experiment_tracking"] is True

    def test_load_config_merges_with_defaults(self, temp_dir):
        roar_dir = temp_dir / ".roar"
        roar_dir.mkdir()
        config_file = roar_dir / "config.toml"
        config_file.write_text("[filters]\nignore_system_reads = false\n")

        config = load_config(start_dir=str(temp_dir))
        assert config["filters"]["ignore_system_reads"] is False
        # Other filter defaults preserved
        assert config["filters"]["ignore_package_reads"] is True


class TestFindConfigFile:
    """Tests for config file discovery."""

    def test_find_config_in_current_dir(self, temp_dir):
        roar_dir = temp_dir / ".roar"
        roar_dir.mkdir()
        config_file = roar_dir / "config.toml"
        config_file.write_text("")

        result = find_config_file(str(temp_dir))
        assert result == config_file

    def test_find_config_walks_up(self, temp_dir):
        # Create config in parent
        roar_dir = temp_dir / ".roar"
        roar_dir.mkdir()
        config_file = roar_dir / "config.toml"
        config_file.write_text("")

        # Create child directory
        child = temp_dir / "subdir"
        child.mkdir()

        result = find_config_file(str(child))
        assert result == config_file

    def test_find_config_returns_none_if_not_found(self, temp_dir):
        result = find_config_file(str(temp_dir))
        assert result is None


class TestSaveConfig:
    """Tests for config saving."""

    def test_save_config_creates_file(self, temp_dir):
        config_file = temp_dir / "config.toml"
        config = {"output": {"track_repo_files": True}, "analyzers": {}, "filters": {}}

        save_config(config, config_file)

        assert config_file.exists()
        content = config_file.read_text()
        assert "track_repo_files = true" in content

    def test_save_config_only_saves_non_defaults(self, temp_dir):
        config_file = temp_dir / "config.toml"
        # All defaults - should result in empty sections
        config = {
            "output": {"track_repo_files": False},
            "analyzers": {"experiment_tracking": True},
            "filters": {
                "ignore_system_reads": True,
                "ignore_package_reads": True,
                "ignore_torch_cache": True,
            },
        }

        save_config(config, config_file)

        content = config_file.read_text()
        # Should be empty or minimal since all are defaults
        assert "track_repo_files = true" not in content


class TestConfigGetSet:
    """Tests for config get/set commands."""

    def test_config_get(self, chdir_temp_roar):
        value = config_get("output.track_repo_files")
        assert value is False

    def test_config_set_bool_true(self, chdir_temp_roar):
        config_path, value = config_set("output.track_repo_files", "true")
        assert value is True
        assert config_path.exists()

        # Verify it persisted
        assert config_get("output.track_repo_files") is True

    def test_config_set_bool_false(self, chdir_temp_roar):
        # First set to true
        config_set("output.track_repo_files", "true")
        # Then back to false
        _config_path, value = config_set("output.track_repo_files", "false")
        assert value is False

    def test_config_set_invalid_key(self, chdir_temp_roar):
        with pytest.raises(ValueError, match="Unknown config key"):
            config_set("invalid.key", "value")

    def test_config_set_invalid_bool(self, chdir_temp_roar):
        with pytest.raises(ValueError, match="Invalid boolean"):
            config_set("output.track_repo_files", "maybe")


class TestGetRoarDir:
    """Tests for get_roar_dir."""

    def test_creates_roar_dir(self, temp_dir):
        roar_dir = get_roar_dir(str(temp_dir))
        assert roar_dir.exists()
        assert roar_dir.name == ".roar"

    def test_returns_existing_roar_dir(self, temp_dir):
        existing = temp_dir / ".roar"
        existing.mkdir()
        (existing / "config.toml").write_text("test")

        roar_dir = get_roar_dir(str(temp_dir))
        assert roar_dir == existing
        # Didn't overwrite
        assert (roar_dir / "config.toml").read_text() == "test"
