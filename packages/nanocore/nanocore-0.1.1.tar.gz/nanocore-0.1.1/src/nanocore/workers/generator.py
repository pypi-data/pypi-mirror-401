import os
import logging
import asyncio
from typing import Dict
from nanocore.worker import Worker

logger = logging.getLogger(__name__)


class GeneratorWorker(Worker):
    def __init__(self):
        super().__init__()
        self.register_handler("scaffold_project", self.handle_scaffold_project)

    async def handle_scaffold_project(self, payload: dict):
        """
        Payload:
        {
            "template": "python_lib",
            "target_dir": "/path/to/new/project",
            "project_name": "my_lib"
        }
        """
        template = payload.get("template")
        target_dir = payload.get("target_dir")
        project_name = payload.get("project_name", "unnamed_project")

        if not template or not target_dir:
            logger.error("Missing template or target_dir in payload.")
            return

        logger.info(
            f"Scaffolding project '{project_name}' using template '{template}' in '{target_dir}'"
        )

        target_path = os.path.abspath(target_dir)

        if not os.path.exists(target_path):
            os.makedirs(target_path)

        if template == "python_lib":
            self._scaffold_python_lib(target_path, project_name)
        else:
            logger.warning(f"Unknown template: {template}")

    def _scaffold_python_lib(self, root: str, name: str):
        # Create structure
        # name/
        #   src/
        #     name/
        #       __init__.py
        #   tests/
        #     __init__.py
        #   pyproject.toml
        #   README.md

        # Sanitize name for directory
        safe_name = name.replace("-", "_").replace(" ", "_")

        src_dir = os.path.join(root, "src", safe_name)
        tests_dir = os.path.join(root, "tests")

        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(tests_dir, exist_ok=True)

        # files
        self._write_file(
            os.path.join(src_dir, "__init__.py"),
            f'"""{name} package."""\n__version__ = "0.1.0"\n',
        )
        self._write_file(os.path.join(tests_dir, "__init__.py"), "")

        readme = f"# {name}\n\nDescription of {name}.\n"
        self._write_file(os.path.join(root, "README.md"), readme)

        pyproject = f"""[project]\nname = \"{name}\"\nversion = \"0.1.0\"\ndescription = \"A python library\"\nreadme = \"README.md\"\nrequires-python = \">=3.10\"\ndependencies = []\n"""
        self._write_file(os.path.join(root, "pyproject.toml"), pyproject)

        logger.info(f"Scaffolded python_lib at {root}")

    def _write_file(self, path, content):
        with open(path, "w") as f:
            f.write(content)
