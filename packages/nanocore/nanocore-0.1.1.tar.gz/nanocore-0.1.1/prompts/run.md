


## Context

The user pass a planning file where planning steps has been describes one by one.

The file contains tasks described in a Markdown format with bulleted ticks (tasks) to organize the specifications.

A tick can have children, which are also ticks, allowing for a hierarchical structure.

Ticks are organized in sequenctial phases.

Example:

## Phase 1: Project Setup and Core Architecture
- [ ] Initialize Python project with `uv` for python 3.12.
- [ ] Configure `pyproject.toml` with dependencies (`fastapi`, `uvicorn`, `python-dotenv`, `websockets`, `pytest`, `pytest-asyncio`).
- [ ] Implement Configuration Loader.
    - [ ] Create `Config` class to load environment variables from `.env` and `.env.example`.
    - [ ] Ensure "Workspace" directory isolation logic is valid.
- [ ] Implement `Worker` Base Class.
    - [ ] Create `Worker` class with an internal `asyncio.Queue`.
    - [ ] Implement the `run` loop to process messages from the queue.
    - [ ] Add signal handling mechanism (asyncio Event) to start/stop processing.
- [ ] Implement `Broker` Class (Basic).
    - [ ] Create `Broker` class.
    - [ ] Implement `register_worker` method.
    - [ ] Implement basic dispatching logic (putting messages into Worker queues).
- [ ] **Verification (Test 01)**: Create a test case for Basic Broker-Worker Lifecycle (Create, Register, Start, Stop).

## Actions

- [ ] parse the file an extract
