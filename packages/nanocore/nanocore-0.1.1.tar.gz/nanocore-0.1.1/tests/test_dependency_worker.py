import pytest
import shutil
import tempfile
import os
import asyncio
from unittest.mock import AsyncMock, patch
from nanocore.workers.dependency import DependencyWorker


@pytest.mark.asyncio
async def test_dependency_worker_python():
    """Test Python dependency installation using uv."""
    # Create a temp dir
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create a simple pyproject.toml
        pyproject_content = """
[project]
name = "test-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
"""
        with open(os.path.join(tmpdirname, "pyproject.toml"), "w") as f:
            f.write(pyproject_content)

        worker = DependencyWorker()

        await worker.handle_install_dependencies({"project_path": tmpdirname})

        # Verify .venv exists (uv sync creates it)
        # Note: 'uv sync' might fail if python version is not compatible or if internet is down.
        # But assuming environment is set up.

        # We check if uv tried to do something.
        if os.path.exists(os.path.join(tmpdirname, ".venv")):
            assert True
        else:
            # If uv failed, it might log error but not crash.
            # We should probably check if it failed or not?
            # The worker logs error but doesn't raise exception to caller in handle_install_dependencies.
            pass
            # For strict testing we might want to assert .venv exists.
            assert os.path.exists(os.path.join(tmpdirname, ".venv"))


@pytest.mark.asyncio
async def test_dependency_worker_rust():
    """Test Rust dependency installation using cargo fetch."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create Cargo.toml
        with open(os.path.join(tmpdirname, "Cargo.toml"), "w") as f:
            f.write("[package]\nname = 'test'\n")

        worker = DependencyWorker()
        with patch.object(worker, "run_subprocess", new_callable=AsyncMock) as mock_run:
            await worker.handle_install_dependencies({"project_path": tmpdirname})
            mock_run.assert_any_call("cargo", ["fetch"], cwd=tmpdirname)


@pytest.mark.asyncio
async def test_dependency_worker_invalid_path():
    """Test behavior when an invalid project path is provided."""
    worker = DependencyWorker()
    # Should not raise exception, just log error
    await worker.handle_install_dependencies({"project_path": "/non/existent/path"})


@pytest.mark.asyncio
async def test_dependency_worker_subprocess_error():
    """Test error handling when a subprocess command fails."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(os.path.join(tmpdirname, "pyproject.toml"), "w") as f:
            f.write("[project]\nname = 'test'\n")

        worker = DependencyWorker()
        with patch.object(worker, "run_subprocess", side_effect=Exception("uv failed")):
            # Should handle exception and log it
            await worker.handle_install_dependencies({"project_path": tmpdirname})


@pytest.mark.asyncio
async def test_dependency_worker_cargo_error():
    """Test error handling when cargo fetch fails."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(os.path.join(tmpdirname, "Cargo.toml"), "w") as f:
            f.write("[package]\nname = 'test'\n")

        worker = DependencyWorker()
        with patch.object(
            worker, "run_subprocess", side_effect=Exception("cargo failed")
        ):
            # Should handle exception and log it
            await worker.handle_install_dependencies({"project_path": tmpdirname})
