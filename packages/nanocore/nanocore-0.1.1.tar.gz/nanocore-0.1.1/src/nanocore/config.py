import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    def __init__(self, env_path: str = ".env"):
        self.env_path = env_path
        load_dotenv(self.env_path)

        # Load workspace directory, default to '.workspace' in the current directory
        self.workspace_dir = Path(os.getenv("WORKSPACE_DIR", ".workspace")).resolve()
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

        # Heartbeat settings
        self.ping_interval = float(os.getenv("PING_INTERVAL", "5.0"))
        self.timeout_threshold = float(os.getenv("TIMEOUT_THRESHOLD", "10.0"))

        # Ensure workspace directory exists
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def resolve_path(self, relative_path: str) -> Path:
        """
        Resolves a relative path within the workspace directory.
        Ensures the path does not escape the workspace (isolation).
        """
        # Join and resolve to get the absolute path
        target_path = (self.workspace_dir / relative_path).resolve()

        # Check if target_path is a subdirectory of workspace_dir
        if not str(target_path).startswith(str(self.workspace_dir)):
            raise ValueError(
                f"Path traversal detected: {relative_path} is outside of workspace {self.workspace_dir}"
            )

        return target_path


# Global config instance
config = Config()
