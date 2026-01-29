import pytest
import os
from pathlib import Path
from nanocore.config import Config


@pytest.fixture
def temp_workspace(tmp_path):
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    return workspace


def test_config_loading_defaults(monkeypatch):
    """Test configuration loading with default values."""
    # Ensure no environment variables interfere
    monkeypatch.delenv("WORKSPACE_DIR", raising=False)
    monkeypatch.delenv("DEBUG", raising=False)

    cfg = Config(env_path="non_existent_env")
    assert cfg.workspace_dir.name == ".workspace"
    assert cfg.debug is False


def test_config_loading_from_env(monkeypatch, tmp_path):
    """Test configuration loading from an environment file."""
    env_file = tmp_path / ".env.test"
    workspace_path = tmp_path / "my_workspace"
    env_file.write_text(f"WORKSPACE_DIR={workspace_path}\nDEBUG=true")

    cfg = Config(env_path=str(env_file))
    assert cfg.workspace_dir == workspace_path.resolve()
    assert cfg.debug is True


def test_resolve_path_valid(temp_workspace, monkeypatch):
    """Test resolving a valid relative path within the workspace."""
    monkeypatch.setenv("WORKSPACE_DIR", str(temp_workspace))
    cfg = Config(env_path="dummy")

    relative = "data/notes.txt"
    resolved = cfg.resolve_path(relative)

    assert resolved == (temp_workspace / relative).resolve()
    # Check that parents were NOT necessarily created by resolve_path (that's intended)
    assert resolved.parent.exists() is False


def test_resolve_path_traversal(temp_workspace, monkeypatch):
    """Test that path traversal attempts raise a ValueError."""
    monkeypatch.setenv("WORKSPACE_DIR", str(temp_workspace))
    cfg = Config(env_path="dummy")

    # Attempting to go outside the workspace
    with pytest.raises(ValueError, match="Path traversal detected"):
        cfg.resolve_path("../outside.txt")

    with pytest.raises(ValueError, match="Path traversal detected"):
        cfg.resolve_path("/etc/passwd")
