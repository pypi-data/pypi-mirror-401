# Test Cases Documentation

This document lists all test cases found in the `tests/` directory.

## `tests/test_app.py`
Tests for the FastAPI application and WebSocket endpoints.

- **test_health_check**: Test the /health endpoint returns correct status and worker count.
- **test_app_state_broker**: Verify that the application state has a properly initialized broker.
- **test_websocket_pong**: Verify that the server accepts a pong message without error.
- **test_websocket_invalid_format**: Verify handling of messages with invalid formats (e.g. missing header).
- **test_websocket_exception_handling**: Verify handling of messages with unexpected data types.

## `tests/test_broker.py`
Tests for the message broker (Worker registration and message dispatching).

- **test_broker_registration**: Verify correct registration of workers and groups.
- **test_dispatch_direct**: Verify direct message dispatch to a specific worker.
- **test_dispatch_broadcast**: Verify broadcast message dispatch to a group of workers.
- **test_dispatch_round_robin**: Verify round-robin message dispatch to a group of workers.
- **test_dispatch_invalid_strategy**: Verify that invalid dispatch strategies raise an error.

## `tests/test_cli.py`
Tests for the Command Line Interface.

- **test_cli_help**: Check that the CLI help command exits successfully.
- **test_cli_connect_help**: Check that the CLI connect command help exits successfully.
- **test_ws_listener_updates_time**: Verify that the WebSocket listener updates the last message time.
- **test_heartbeat_sends_pong**: Verify that the heartbeat loop sends a pong response when active.
- **test_heartbeat_timeout**: Verify that the heartbeat loop detects a timeout and closes the connection.
- **test_shell_loop_shortcuts**: Test shell loop shortcut commands like 'push' and 'add'.
- **test_shell_loop_json**: Test shell loop handling of raw JSON input.
- **test_shell_loop_edge_cases**: Test shell loop handling of edge cases and invalid inputs.
- **test_ws_listener_invalid_json**: Verify that the WebSocket listener handles invalid JSON gracefully.
- **test_ws_listener_error**: Verify that the WebSocket listener handles general exceptions gracefully.
- **test_heartbeat_error**: Verify that the heartbeat loop handles send errors gracefully.
- **test_run_client_flow**: Test the overall client execution flow including connection and sub-tasks.
- **test_run_client_connection_failure**: Test that the client exits with an error code on connection failure.

## `tests/test_code_ops_worker.py`
Tests for the Code Operations Worker.

- **test_code_ops_format_python**: Test Python code formatting using Ruff.

## `tests/test_config.py`
Tests for configuration loading and path resolution.

- **test_config_loading_defaults**: Test configuration loading with default values.
- **test_config_loading_from_env**: Test configuration loading from an environment file.
- **test_resolve_path_valid**: Test resolving a valid relative path within the workspace.
- **test_resolve_path_traversal**: Test that path traversal attempts raise a ValueError.

## `tests/test_dependency_worker.py`
Tests for the Dependency Worker.

- **test_dependency_worker_python**: Test Python dependency installation using uv.
- **test_dependency_worker_rust**: Test Rust dependency installation using cargo fetch.
- **test_dependency_worker_invalid_path**: Test behavior when an invalid project path is provided.
- **test_dependency_worker_subprocess_error**: Test error handling when a subprocess command fails.

## `tests/test_fuzz_broker.py`
Fuzz tests for the Broker using Hypothesis.

- **test_broker_no_crash_fuzz**: Fuzz test to ensure the broker does not crash under random sequences of actions.
- **test_broker_round_robin_fairness_fuzz**: Verify round-robin dispatch fairness with multiple workers.
- **test_broker_broadcast_coverage_fuzz**: Verify that broadcast messages reach all registered workers in a group.

## `tests/test_fuzz_rpn.py`
Fuzz tests for the RPN Worker using Hypothesis.

- **test_rpn_fuzz_logic**: Fuzz test for RPN stack logic and operations.
- **test_rpn_division_by_zero_invariant**: Test division by zero invariant (pops 2, pushes 2 back if div by zero).
- **test_rpn_no_exceptions**: Test that no combination of inputs causes an unhandled exception.

## `tests/test_generator_worker.py`
Tests for the Project Generator Worker.

- **test_generator_python_lib**: Test Python library project scaffolding.

## `tests/test_heartbeat.py`
Tests for WebSocket heartbeat mechanism (Integration style using TestClient).

- **test_websocket_heartbeat**: Test full ping/pong cycle via TestClient.
- **test_websocket_timeout**: Verify server disconnects client after timeout.

## `tests/test_integration_rpn.py`
Integration tests for RPN functionality.

- **test_rpn_integration**: Test RPN worker integrated with Broker using various dispatch strategies.

## `tests/test_integration_sha1.py`
Integration tests for SHA1 worker.

- **test_integration_sha1_load**: Test SHA1 worker load distribution with multiple workers and round-robin dispatch.

## `tests/test_multi_worker.py`
Integration tests involving multiple worker types.

- **test_multi_worker_concurrent_processing**: Test involving 2 running workers to verify concurrent operation, routing, and shared handlers.

## `tests/test_rpn_worker.py`
Unit tests for the RPN Worker.

- **test_rpn_basic_ops**: Test basic RPN operations (push, add, mul).
- **test_rpn_sub_div**: Test subtraction and division operations.
- **test_rpn_insufficient_operands**: Test handling of insufficient operands.
- **test_rpn_clear**: Test clearing the stack.

## `tests/test_subprocess_worker.py`
Tests for the Subprocess Worker utility.

- **test_run_subprocess_echo**: Test running a simple echo subprocess.
- **test_run_subprocess_fail**: Test behavior when a subprocess fails (checking return codes and exceptions).

## `tests/test_task_worker.py`
Tests for the Task Automation Worker.

- **test_task_pipeline_success**: Test successful execution of a task pipeline.
- **test_task_pipeline_stop_on_error**: Test pipeline stopping when a task fails.
- **test_task_pipeline_continue_on_error**: Test pipeline continuing when a task fails.
- **test_task_pipeline_skip_invalid**: Test skipping invalid tasks in a pipeline.

## `tests/test_worker.py`
Unit tests for the base Worker class.

- **test_worker_start_stop**: Test worker start, stop, and running signal states.
- **test_worker_message_processing**: Test basic message processing loop.
- **test_worker_multiple_handlers**: Test registering and triggering multiple handlers.
- **test_worker_no_type**: Test handling of messages with missing message type.
- **test_worker_handler_exception**: Test handling of exceptions raised within handlers.
- **test_worker_run_cancelled**: Test cancellation of the worker run task.
- **test_worker_no_handler**: Test handling of messages with no matching registered handler.
