import os
import logging
from nanocore.subprocess_worker import SubprocessWorker

logger = logging.getLogger(__name__)


class CodeOpsWorker(SubprocessWorker):
    def __init__(self):
        super().__init__()
        self.register_handler("format", self.handle_format)
        self.register_handler("lint", self.handle_lint)

    async def handle_format(self, payload: dict):
        path = payload.get("path", ".")
        path = os.path.abspath(path)

        logger.info(f"Formatting code at {path}")

        # Python: ruff format
        try:
            # ruff format works recursively on directories or on specific files
            await self.run_subprocess("ruff", ["format", path], check=False)
        except FileNotFoundError:
            logger.warning("ruff not found. Skipping Python formatting.")
        except Exception as e:
            logger.error(f"Error running ruff format: {e}")

        # Rust: rustfmt / cargo fmt
        if os.path.isdir(path):
            if os.path.exists(os.path.join(path, "Cargo.toml")):
                try:
                    await self.run_subprocess("cargo", ["fmt"], cwd=path, check=False)
                except Exception as e:
                    logger.error(f"Error running cargo fmt: {e}")
            else:
                # Iterate or glob for .rs? Or just assume user points to file?
                # If path is dir and no Cargo.toml, maybe skip rust for now or rely on user being specific.
                pass
        elif path.endswith(".rs"):
            try:
                await self.run_subprocess("rustfmt", [path], check=False)
            except Exception as e:
                logger.error(f"Error running rustfmt: {e}")

    async def handle_lint(self, payload: dict):
        path = payload.get("path", ".")
        path = os.path.abspath(path)

        logger.info(f"Linting code at {path}")

        # Python: ruff check
        try:
            await self.run_subprocess("ruff", ["check", path], check=False)
        except FileNotFoundError:
            logger.warning("ruff not found. Skipping Python linting.")
        except Exception as e:
            logger.error(f"Error running ruff check: {e}")

        # Rust: cargo check
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "Cargo.toml")):
            try:
                await self.run_subprocess("cargo", ["check"], cwd=path, check=False)
            except Exception as e:
                logger.error(f"Error running cargo check: {e}")
