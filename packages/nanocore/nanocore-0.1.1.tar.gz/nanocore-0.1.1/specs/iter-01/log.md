


# 2026-01-10

- [[000.kickoff]]
- [x] create a cookiecutter template from this project
- [ ] expand a live project with current template
- [ ] update the original template
- [ ] sync `cookiecutter` template
- [ ] 

# 2026-01-11

- [x] **1.1. Project Structure Setup**
- [x] **1.2. Configuration Management**
- [x] **1.3. Database Infrastructure**
- [x] **2.1. Schema Definition**
- [x] **2.2. Database Abstraction**
- [x] **3.1. Markdown Parser**
- [x] **3.2. Dependency Graph Builder**
- [x] **3.3. File System Watcher**
- [x] **3.4. Orchestrator Logic**
- [x] **4.1. Input Preparation**
- [x] **4.2. Output Capture & Throttling**
- [x] **4.3. Action Executors**
- [x] **4.4. Async Runner Service**
- [x] **5.1. Basic Endpoints**
- [x] **5.2. Authentication**
- [x] **6.1. CLI Client**
- [x] **6.2. CI/CD & Documentation**


TODO:
- [ ] setup `.gitignore`
- [ ] create a branch for each step
- [ ] update the project
- [ ] steps verifications
- [ ] git commits must be done at the end of each step
- [ ] merge files such `.env` from `.env.example`
- [ ] generate CI/CD yaml workflows for GitLab
- [ ] full tests pass before commit files on every step
- [ ] detect which files must be commited on each step since the last commit.
- [ ] on every commit, run tests and linting
- [ ] on every commit, catpture the progress made by the AI



Example

```bash
Progress Updates
1 Creating docker-compose.yml for SurrealDB.
2 Updating .env and adding surrealdb dependency.
3 Implementing SurrealDB client in src/db/session.py.
4 Starting SurrealDB and verifying connection.
5 Starting SurrealDB using 'docker compose' and verifying connection.
6 Updating src/db/session.py to use AsyncSurreal.
7 Fixing return type hint in src/db/session.py.
8 Fixing signin parameters in src/db/session.py.
9 Finalizing documentation and completing Phase 1.3.
```

```bash
Progress Updates
1 Implementing Pydantic models for tasks and executions.
2 Creating tests for repositories and atomic claim logic.
3 Adding pytest-asyncio and running repository tests.
4 Configuring pytest-asyncio in pyproject.toml.
5 Updating tests to use pytest_asyncio.fixture and updating pyproject.toml.
6 Fixing imports and pyproject.toml configuration.
7 Changing fixture scope to 'function' to fix ScopeMismatch.
8 Fixing repository create method to handle SurrealDB result correctly.
9 Updating repository to handle SurrealDB RecordID objects.
10 Fixing imports in src/db/repository.py.
11 Fixing repository methods and query syntax.
12 Updating claim_task query to use LET statement for better atomicity and compatibility.
13 Updating claim_task query to use a single-statement atomic update.
14 Debugging claim_task by printing the response from SurrealDB.
15 Fixing claim_task result handling based on debug output.
16 Cleaning up pyproject.toml and finalizing Phase 2.2.
```


- [ ] analyze `uv run ptw . --` (or a single pytest execution) to check for code coverage and identify potential issues.
- [ ] track code coverage con every commit. Include coverage in the commit message.
- [ ] order to AI to improve the lower coverage in the full report, so coverage percent is balanced between different files and modules.

Example:

Put in `pyproject.toml`

```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=your_package_name",
    "--cov-report=term-missing",
    "--cov-report=html",      # optional
    "--cov-fail-under=85",    # optional: fail build if coverage < 85%
]

# Exclude tests from coverage (add to pyproject.toml or .coveragerc)
[tool.coverage.run] omit = ["tests/*", "*__init__.py"]
```

```bash
agp@dev00:~/vault/procode$ uv run pytest
==================================================== test session starts =====================================================
platform linux -- Python 3.12.9, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/agp/vault/procode
configfile: pyproject.toml
plugins: cov-7.0.0, asyncio-1.3.0, anyio-4.12.1
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 22 items

tests/test_config.py ..                                                                                                [  9%]
tests/test_graph.py ....                                                                                               [ 27%]
tests/test_input_builder.py ...                                                                                        [ 40%]
tests/test_orchestrator.py ...                                                                                         [ 54%]
tests/test_parser.py .....                                                                                             [ 77%]
tests/test_repository.py ...                                                                                           [ 90%]
tests/test_watcher.py ..                                                                                               [100%]

======================================================= tests coverage =======================================================
______________________________________ coverage: platform linux, python 3.12.9-final-0 _______________________________________

Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/api/__init__.py                0      0   100%
src/core/__init__.py               0      0   100%
src/core/config.py                14      0   100%
src/core/models.py                36      0   100%
src/core/orchestrator.py          62      9    85%   33, 39, 54-56, 83-84, 94, 109-110
src/core/watcher.py               44      2    95%   47, 71
src/db/__init__.py                 0      0   100%
src/db/repository.py              68      9    87%   16, 32, 40, 43, 68-69, 77, 89, 96
src/db/session.py                 32      5    84%   21-23, 33, 40
src/db/verify_connection.py       21     21     0%   1-26
src/runners/__init__.py            0      0   100%
src/runners/input_builder.py      37      7    81%   40-44, 57-59
src/utils/__init__.py              0      0   100%
src/utils/graph.py                30      0   100%
src/utils/parser.py               15      0   100%
------------------------------------------------------------
TOTAL                            359     53    85%
Coverage HTML written to dir htmlcov
Required test coverage of 85% reached. Total coverage: 85.24%
===================================================== 22 passed in 2.95s =====================================================
agp@dev00:~/vault/procode$
```


Better coverage

```bash
# Install the magic combo
uv add --dev pytest-testmon pytest-watcher

# Run in watch mode → automatically runs only affected + previously failing tests
uv run ptw . -- --testmon

# Or one-shot fast mode:
uv run pytest --testmon
```
