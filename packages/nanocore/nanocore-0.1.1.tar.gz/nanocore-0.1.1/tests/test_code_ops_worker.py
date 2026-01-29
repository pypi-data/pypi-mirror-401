import pytest
import tempfile
import os
from unittest.mock import AsyncMock, patch
from nanocore.workers.code_ops import CodeOpsWorker


@pytest.mark.asyncio
async def test_code_ops_format_python():
    """Test Python code formatting using Ruff."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        messy_code = "x=1\ny=  2\ndef func():\n return x+y\n"
        file_path = os.path.join(tmpdirname, "messy.py")
        with open(file_path, "w") as f:
            f.write(messy_code)

        worker = CodeOpsWorker()
        await worker.handle_format({"path": file_path})

        with open(file_path, "r") as f:
            formatted_code = f.read()

        assert "x = 1" in formatted_code
        assert "y = 2" in formatted_code


@pytest.mark.asyncio
async def test_code_ops_format_rust_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(os.path.join(tmpdirname, "Cargo.toml"), "w") as f:
            f.write("[package]\nname = 'test'\n")

        worker = CodeOpsWorker()
        with patch.object(worker, "run_subprocess", new_callable=AsyncMock) as mock_run:
            await worker.handle_format({"path": tmpdirname})
            mock_run.assert_any_call("cargo", ["fmt"], cwd=tmpdirname, check=False)


@pytest.mark.asyncio
async def test_code_ops_format_rust_file():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = os.path.join(tmpdirname, "main.rs")
        with open(file_path, "w") as f:
            f.write("fn main(){}")

        worker = CodeOpsWorker()
        with patch.object(worker, "run_subprocess", new_callable=AsyncMock) as mock_run:
            await worker.handle_format({"path": file_path})
            mock_run.assert_any_call("rustfmt", [file_path], check=False)


@pytest.mark.asyncio
async def test_code_ops_lint_python():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = os.path.join(tmpdirname, "test.py")
        with open(file_path, "w") as f:
            f.write("import os\n")

        worker = CodeOpsWorker()
        with patch.object(worker, "run_subprocess", new_callable=AsyncMock) as mock_run:
            await worker.handle_lint({"path": file_path})
            mock_run.assert_any_call("ruff", ["check", file_path], check=False)


@pytest.mark.asyncio
async def test_code_ops_lint_rust():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(os.path.join(tmpdirname, "Cargo.toml"), "w") as f:
            f.write("[package]\nname = 'test'\n")

        worker = CodeOpsWorker()
        with patch.object(worker, "run_subprocess", new_callable=AsyncMock) as mock_run:
            await worker.handle_lint({"path": tmpdirname})
            mock_run.assert_any_call("cargo", ["check"], cwd=tmpdirname, check=False)


@pytest.mark.asyncio
async def test_code_ops_ruff_not_found():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = os.path.join(tmpdirname, "test.py")
        with open(file_path, "w") as f:
            f.write("x=1")

        worker = CodeOpsWorker()
        with patch.object(worker, "run_subprocess", side_effect=FileNotFoundError):
            await worker.handle_format({"path": file_path})
            await worker.handle_lint({"path": file_path})


@pytest.mark.asyncio
async def test_code_ops_ruff_format_exception():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = os.path.join(tmpdirname, "test.py")
        with open(file_path, "w") as f:
            f.write("x=1")
        worker = CodeOpsWorker()
        with patch.object(
            worker, "run_subprocess", side_effect=Exception("format error")
        ):
            await worker.handle_format({"path": file_path})


@pytest.mark.asyncio
async def test_code_ops_cargo_fmt_exception():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(os.path.join(tmpdirname, "Cargo.toml"), "w") as f:
            f.write("[package]")
        worker = CodeOpsWorker()
        with patch.object(
            worker, "run_subprocess", side_effect=Exception("cargo error")
        ):
            await worker.handle_format({"path": tmpdirname})


@pytest.mark.asyncio
async def test_code_ops_rustfmt_exception():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = os.path.join(tmpdirname, "main.rs")
        with open(file_path, "w") as f:
            f.write("fn main(){}")
        worker = CodeOpsWorker()
        with patch.object(
            worker, "run_subprocess", side_effect=Exception("rustfmt error")
        ):
            await worker.handle_format({"path": file_path})


@pytest.mark.asyncio
async def test_code_ops_format_dir_no_cargo():
    with tempfile.TemporaryDirectory() as tmpdirname:
        worker = CodeOpsWorker()
        with patch.object(worker, "run_subprocess", new_callable=AsyncMock) as mock_run:
            await worker.handle_format({"path": tmpdirname})
            cargo_calls = [c for c in mock_run.call_args_list if "cargo" in str(c)]
            assert len(cargo_calls) == 0


@pytest.mark.asyncio
async def test_code_ops_ruff_check_exception():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = os.path.join(tmpdirname, "test.py")
        with open(file_path, "w") as f:
            f.write("x=1")
        worker = CodeOpsWorker()
        with patch.object(
            worker, "run_subprocess", side_effect=Exception("check error")
        ):
            await worker.handle_lint({"path": file_path})


@pytest.mark.asyncio
async def test_code_ops_cargo_check_exception():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(os.path.join(tmpdirname, "Cargo.toml"), "w") as f:
            f.write("[package]")
        worker = CodeOpsWorker()
        with patch.object(
            worker, "run_subprocess", side_effect=Exception("cargo check error")
        ):
            await worker.handle_lint({"path": tmpdirname})


@pytest.mark.asyncio
async def test_code_ops_lint_default_path():
    worker = CodeOpsWorker()
    with patch.object(worker, "run_subprocess", new_callable=AsyncMock):
        await worker.handle_lint({})
