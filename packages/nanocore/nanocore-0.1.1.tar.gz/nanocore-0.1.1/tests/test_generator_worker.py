import pytest
import tempfile
import os
from nanocore.workers.generator import GeneratorWorker


@pytest.mark.asyncio
async def test_generator_python_lib():
    with tempfile.TemporaryDirectory() as tmpdirname:
        worker = GeneratorWorker()
        project_dir = os.path.join(tmpdirname, "my-lib")

        await worker.handle_scaffold_project(
            {
                "template": "python_lib",
                "target_dir": project_dir,
                "project_name": "my-lib",
            }
        )

        assert os.path.exists(os.path.join(project_dir, "pyproject.toml"))
        # Expect hyphen replaced by underscore in src path
        assert os.path.exists(os.path.join(project_dir, "src", "my_lib", "__init__.py"))
        assert os.path.exists(os.path.join(project_dir, "tests", "__init__.py"))
        assert os.path.exists(os.path.join(project_dir, "README.md"))


@pytest.mark.asyncio
async def test_generator_missing_payload():
    worker = GeneratorWorker()
    # Missing template
    await worker.handle_scaffold_project({"target_dir": "/tmp/test"})
    # Missing target_dir
    await worker.handle_scaffold_project({"template": "python_lib"})


@pytest.mark.asyncio
async def test_generator_unknown_template():
    with tempfile.TemporaryDirectory() as tmpdirname:
        worker = GeneratorWorker()
        await worker.handle_scaffold_project(
            {"template": "unknown", "target_dir": tmpdirname, "project_name": "test"}
        )
        # Should not crash, just log warning
