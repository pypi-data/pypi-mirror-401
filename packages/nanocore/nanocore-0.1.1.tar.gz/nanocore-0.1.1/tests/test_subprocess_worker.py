import pytest
import asyncio
from nanocore.subprocess_worker import SubprocessWorker


@pytest.mark.asyncio
async def test_run_subprocess_echo():
    worker = SubprocessWorker()
    code, out, err = await worker.run_subprocess("echo", ["hello"])
    assert code == 0
    assert out == "hello"
    assert err == ""


@pytest.mark.asyncio
async def test_run_subprocess_stderr():
    worker = SubprocessWorker()
    # Use shell to redirect to stderr
    code, out, err = await worker.run_subprocess("sh", ["-c", "echo error >&2"])
    assert code == 0
    assert out == ""
    assert err == "error"


@pytest.mark.asyncio
async def test_run_subprocess_fail():
    worker = SubprocessWorker()
    # verify check=True raises exception with stderr in message
    with pytest.raises(RuntimeError) as excinfo:
        await worker.run_subprocess(
            "sh", ["-c", "echo some error >&2; exit 1"], check=True
        )
    assert "some error" in str(excinfo.value)
    assert "exit code 1" in str(excinfo.value)

    # verify check=False returns code
    code, _, _ = await worker.run_subprocess("false", [], check=False)
    assert code != 0


@pytest.mark.asyncio
async def test_run_subprocess_not_found():
    worker = SubprocessWorker()
    with pytest.raises(FileNotFoundError) as excinfo:
        await worker.run_subprocess("non_existent_program_12345", [])
    assert "Executable not found" in str(excinfo.value)
