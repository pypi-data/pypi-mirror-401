#!/usr/bin/env python3
import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path
from typing import List


class PromptFinder:
    """Responsible for locating prompt files."""

    def __init__(self, search_pattern: str = "*prompt.md"):
        self.search_pattern = search_pattern

    def find(self, directory: str = ".") -> List[Path]:
        """Find all prompt files and sort them"""
        return sorted(Path(directory).rglob(self.search_pattern))


class PromptRunner:
    """Encapsulates the execution of gemini command for a single prompt file."""

    # ANSI color codes
    PINK = "\033[38;5;207m"  # bright pink/magenta
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.filepath_str = str(file_path)

    def _run_command(self, cmd: str) -> int:
        """Run shell command and return its exit code"""
        try:
            # Note: Parallel execution might interleve output from different processes.
            # Using Popen with PIPE and reading line by line is okay for basic streaming,
            # but users might see mixed lines if multiple runners output at once.
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # merge stderr into stdout
                text=True,
                bufsize=1,  # line buffered
                universal_newlines=True,
            )

            # Print output line by line as it comes
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    print(line, end="", flush=True)  # real-time printing

            return_code = process.wait()
            return return_code
        except Exception as e:
            print(
                f"{self.RED}Failed to execute command: {e}{self.RESET}", file=sys.stderr
            )
            return 1

    def run(self) -> int:
        """Execute the processing for the assigned prompt file. Returns exit code."""
        print(f"{self.PINK}{'=' * 49}{self.RESET}")
        print(f"{self.PINK}Processing: {self.filepath_str}{self.RESET}")
        print(f"{self.PINK}{'=' * 49}{self.RESET}")

        # The command we want to run
        cmd = f'gemini -o stream-json "read the prompt in {self.filepath_str!r} file and do the actions described"'

        print(cmd)

        exit_code = self._run_command(cmd)

        if exit_code == 0:
            print(f"{self.GREEN}{'-' * 49}{self.RESET}")
            print(f"{self.GREEN}done: {self.filepath_str}{self.RESET}")
            print(f"{self.GREEN}{'-' * 49}{self.RESET}")
        else:
            print(
                f"{self.RED}Error: command failed (exit code {exit_code}) for {self.filepath_str}{self.RESET}",
                file=sys.stderr,
            )

        return exit_code


def main():
    parser = argparse.ArgumentParser(description="Process prompt files in parallel.")
    parser.add_argument(
        "-p",
        "--parallel",
        type=int,
        default=1,
        help="Number of parallel runners (default: 1)",
    )
    parser.add_argument(
        "-i", "--iteration", type=int, default=1, help="Iteration number"
    )
    args = parser.parse_args()

    print(f"Running (parallelism: {args.parallel})...")

    iteration = args.iteration
    iteration_str = f"{iteration:02d}"

    finder = PromptFinder()
    path = f"specs/iter-{iteration_str}/"
    prompt_files = finder.find(path)

    if not prompt_files:
        print(f"No {finder.search_pattern} files found")
        return

    # Use ThreadPoolExecutor to run runners in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
        # Create runner instances
        runners = [PromptRunner(fp) for fp in prompt_files]

        # Submit tasks to executor
        future_to_runner = {executor.submit(runner.run): runner for runner in runners}

        overall_success = True
        for future in concurrent.futures.as_completed(future_to_runner):
            runner = future_to_runner[future]
            try:
                exit_code = future.result()
                if exit_code != 0:
                    overall_success = False
            except Exception as exc:
                print(
                    f"{PromptRunner.RED}Runner for {runner.filepath_str} generated an exception: {exc}{PromptRunner.RESET}"
                )
                overall_success = False

    if not overall_success:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)
