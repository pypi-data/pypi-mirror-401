import logging
from typing import List, Dict, Any
from nanocore.subprocess_worker import SubprocessWorker

logger = logging.getLogger(__name__)


class TaskAutomationWorker(SubprocessWorker):
    def __init__(self):
        super().__init__()
        self.register_handler("run_pipeline", self.handle_run_pipeline)
        self.pipeline_history: List[Dict[str, Any]] = []

    async def handle_run_pipeline(self, payload: dict):
        """
        Payload schema:
        {
            "tasks": [
                {
                    "name": "Task Name",
                    "command": "cmd",
                    "args": ["arg1", "arg2"],
                    "cwd": "optional/path"
                },
                ...
            ],
            "stop_on_error": True (default)
        }
        """
        tasks = payload.get("tasks", [])
        stop_on_error = payload.get("stop_on_error", True)

        logger.info(f"Starting pipeline with {len(tasks)} tasks.")

        pipeline_results = {"tasks": [], "status": "success"}

        for i, task in enumerate(tasks):
            name = task.get("name", f"Task {i}")
            command = task.get("command")
            args = task.get("args", [])
            cwd = task.get("cwd")

            if not command:
                logger.warning(f"Task {name} has no command. Skipping.")
                pipeline_results["tasks"].append(
                    {"name": name, "status": "skipped", "reason": "no command provided"}
                )
                continue

            logger.info(f"Running task: {name}")

            task_result = {
                "name": name,
                "command": command,
                "args": args,
                "status": "pending",
            }

            try:
                retcode, stdout, stderr = await self.run_subprocess(
                    command, args, cwd=cwd, check=stop_on_error
                )
                task_result.update(
                    {
                        "status": "success" if retcode == 0 else "failed",
                        "return_code": retcode,
                        "stdout": stdout,
                        "stderr": stderr,
                    }
                )
                if retcode != 0:
                    pipeline_results["status"] = "failed"
            except Exception as e:
                logger.error(f"Task '{name}' failed: {e}")
                task_result.update({"status": "failed", "error": str(e)})
                pipeline_results["status"] = "failed"
                pipeline_results["tasks"].append(task_result)

                if stop_on_error:
                    logger.error("Stopping pipeline due to error.")
                    self.pipeline_history.append(pipeline_results)
                    return pipeline_results
                continue

            pipeline_results["tasks"].append(task_result)

        logger.info("Pipeline completed.")
        self.pipeline_history.append(pipeline_results)
        return pipeline_results
