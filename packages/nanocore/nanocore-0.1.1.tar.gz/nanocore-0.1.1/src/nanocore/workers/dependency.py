import os
import logging
from nanocore.subprocess_worker import SubprocessWorker

logger = logging.getLogger(__name__)


class DependencyWorker(SubprocessWorker):
    def __init__(self):
        super().__init__()
        self.register_handler("install_dependencies", self.handle_install_dependencies)

    async def handle_install_dependencies(self, payload: dict):
        project_path = payload.get("project_path", ".")
        project_path = os.path.abspath(project_path)

        logger.info(f"Installing dependencies for project at {project_path}")

        if not os.path.exists(project_path):
            logger.error(f"Project path does not exist: {project_path}")
            return

        # Python (uv)
        if os.path.exists(os.path.join(project_path, "pyproject.toml")):
            logger.info("Found pyproject.toml, running 'uv sync'...")
            try:
                await self.run_subprocess("uv", ["sync"], cwd=project_path)
                logger.info("Python dependencies installed successfully.")
            except Exception as e:
                logger.error(f"Failed to install Python dependencies: {e}")

        # Rust (cargo)
        if os.path.exists(os.path.join(project_path, "Cargo.toml")):
            logger.info("Found Cargo.toml, running 'cargo fetch'...")
            try:
                await self.run_subprocess("cargo", ["fetch"], cwd=project_path)
                logger.info("Rust dependencies fetched successfully.")
            except Exception as e:
                logger.error(f"Failed to fetch Rust dependencies: {e}")
