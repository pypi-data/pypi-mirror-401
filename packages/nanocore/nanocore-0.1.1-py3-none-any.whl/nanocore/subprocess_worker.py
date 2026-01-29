import asyncio
import logging
from typing import List, Optional, Tuple, Union

from nanocore.worker import Worker

logger = logging.getLogger(__name__)


class SubprocessWorker(Worker):
    """
    Worker specialized in running subprocesses.
    """

    async def run_subprocess(
        self,
        program: str,
        args: List[str],
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
        check: bool = True,
    ) -> Tuple[int, str, str]:
        """
        Executes a subprocess.

        Args:
            program: The program to execute.
            args: List of arguments.
            cwd: Working directory.
            env: Environment variables.
            check: If True, raises Exception on non-zero exit code.

        Returns:
            Tuple containing (return_code, stdout, stderr)
        """
        logger.info(f"Running subprocess: {program} {args} in {cwd or 'default cwd'}")

        try:
            process = await asyncio.create_subprocess_exec(
                program,
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=env,
            )

            stdout_data, stderr_data = await process.communicate()

            stdout_str = stdout_data.decode().strip()
            stderr_str = stderr_data.decode().strip()

            if stdout_str:
                logger.debug(f"[{program}] STDOUT: {stdout_str}")
            if stderr_str:
                logger.debug(f"[{program}] STDERR: {stderr_str}")

            if check and process.returncode != 0:
                error_msg = f"Command '{program} {' '.join(args)}' failed with exit code {process.returncode}: {stderr_str or stdout_str}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            return process.returncode, stdout_str, stderr_str

        except FileNotFoundError:
            error_msg = f"Executable not found: {program}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        except Exception as e:
            logger.error(f"Subprocess execution failed: {e}")
            raise
