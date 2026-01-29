import asyncio
import json
import logging
import time
from typing import Optional
import typer
import websockets
from rich.console import Console

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Constants
DEFAULT_URL = "ws://localhost:8000/ws"
HEARTBEAT_INTERVAL = 5.0
TIMEOUT_THRESHOLD = 10.0

app = typer.Typer(help="Nanocore CLI - Asynchronous Knowledge Base Tool.")
console = Console()


class ClientState:
    def __init__(self):
        self.last_msg_time = time.time()
        self.is_connected = False
        self.catalog_response = None


state = ClientState()


async def ws_listener(websocket: websockets.WebSocketClientProtocol):
    """Listens for server messages and updates last message time."""
    try:
        async for message in websocket:
            state.last_msg_time = time.time()
            try:
                data = json.loads(message)
                if data.get("type") == "ping":
                    logger.debug("Received ping from server")
                    # We respond with pong in the heartbeat loop or here.
                    # The requirement says "Task to send pong or ping every 5s".
                    # Let's handle it in the heartbeat loop to be consistent with "Task".
                elif data.get("header", {}).get("msg_type") == "catalog_response":
                    state.catalog_response = data.get("body", {})
                    logger.debug("Received catalog response")
                else:
                    console.print(f"[cyan]Server:[/cyan] {data}")
            except json.JSONDecodeError:
                console.print(f"[yellow]Raw Server:[/yellow] {message}")
    except websockets.exceptions.ConnectionClosed:
        console.print("[red]Connection closed by server.[/red]")
    except Exception as e:
        logger.error(f"Listener error: {e}")
    finally:
        state.is_connected = False


async def heartbeat_loop(websocket: websockets.WebSocketClientProtocol):
    """Sends pings and checks for server disconnection."""
    logger.info("Client heartbeat loop started.")
    try:
        while state.is_connected:
            # 1. Send pong to server (or ping, but server sends ping, so we send pong)
            # The requirement: "Task to send pong or ping every 5 seconds"
            try:
                await websocket.send(
                    json.dumps({"type": "pong", "timestamp": time.time()})
                )
                logger.debug("Sent pong to server")
            except Exception as e:
                logger.error(f"Failed to send heartbeat: {e}")
                break

            await asyncio.sleep(HEARTBEAT_INTERVAL)

            # 2. Check for server timeout
            now = time.time()
            if now - state.last_msg_time > TIMEOUT_THRESHOLD:
                console.print(
                    f"[red]Server timeout detected ({now - state.last_msg_time:.1f}s). Disconnecting.[/red]"
                )
                break
    except asyncio.CancelledError:
        logger.info("Heartbeat loop cancelled.")
    finally:
        if state.is_connected:
            await websocket.close()
            state.is_connected = False


from nanocore.schema import create_message


def _display_catalog(catalog: dict):
    """Display the service catalog using Rich tables."""
    from rich.table import Table

    # Workers table
    workers_table = Table(title="Available Workers")
    workers_table.add_column("Worker ID", style="cyan")
    workers_table.add_column("Groups", style="green")
    workers_table.add_column("Handlers", style="yellow")

    for worker_id, info in catalog.get("workers", {}).items():
        groups = ", ".join(info.get("groups", [])) or "-"
        handlers = ", ".join(info.get("handlers", [])) or "-"
        workers_table.add_row(worker_id, groups, handlers)

    console.print(workers_table)

    # Groups table
    if catalog.get("groups"):
        groups_table = Table(title="Worker Groups")
        groups_table.add_column("Group Name", style="magenta")
        groups_table.add_column("Workers", style="cyan")

        for group, worker_ids in catalog.get("groups", {}).items():
            workers = ", ".join(worker_ids)
            groups_table.add_row(group, workers)

        console.print(groups_table)


async def shell_loop(websocket: websockets.WebSocketClientProtocol):
    """Interactive shell for sending messages."""
    console.print("[bold green]Interactive Shell Started.[/bold green]")
    console.print(
        "Commands: [bold]catalog, push <val>, add, sub, mul, div, clear, disconnect, quit[/bold]"
    )
    console.print("Or enter raw JSON starting with [bold]{[/bold]")

    try:
        while state.is_connected:
            # We use to_thread because input() is blocking
            user_input = await asyncio.to_thread(input, "nanocore> ")
            user_input = user_input.strip()

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit"):
                state.is_connected = False
                break

            if user_input.lower() == "disconnect":
                console.print("[yellow]Disconnecting...[/yellow]")
                state.is_connected = False
                break

            msg_payload = None
            msg_type = None

            if user_input.startswith("{"):
                try:
                    raw_msg = json.loads(user_input)
                    if "type" in raw_msg:
                        msg_type = raw_msg.pop("type")
                        msg_payload = raw_msg
                    else:
                        console.print(
                            "[red]JSON message must contain a 'type' field.[/red]"
                        )
                except json.JSONDecodeError as e:
                    console.print(f"[red]Invalid JSON: {e}[/red]")
            else:
                # Basic shortcuts for RPN
                parts = user_input.split()
                cmd = parts[0].lower()
                if cmd == "push" and len(parts) > 1:
                    try:
                        val = float(parts[1])
                        msg_type = "push"
                        msg_payload = {"value": val}
                    except ValueError:
                        console.print("[red]Value must be a number[/red]")
                elif cmd == "catalog":
                    # Request catalog
                    msg = create_message(
                        msg_type="get_catalog", body={}, sender="cli-client"
                    )
                    await websocket.send(json.dumps(msg))

                    # Wait briefly for response
                    await asyncio.sleep(0.5)

                    # Display catalog
                    if state.catalog_response:
                        _display_catalog(state.catalog_response)
                        state.catalog_response = None
                    else:
                        console.print("[yellow]No catalog response received[/yellow]")
                    continue
                elif cmd in ("add", "sub", "mul", "div", "clear"):
                    msg_type = cmd
                    msg_payload = {}
                else:
                    console.print(
                        f"[yellow]Unknown command or invalid format: {cmd}[/yellow]"
                    )

            if msg_type:
                msg = create_message(
                    msg_type=msg_type, body=msg_payload, sender="cli-client"
                )
                await websocket.send(json.dumps(msg))
                logger.debug(f"Sent message: {msg}")

    except EOFError:
        pass
    except Exception as e:
        logger.error(f"Shell error: {e}")
    finally:
        state.is_connected = False


async def run_client(url: str):
    """Main client loop."""
    try:
        async with websockets.connect(url) as websocket:
            state.is_connected = True
            state.last_msg_time = time.time()
            console.print(f"[green]Connected to {url}[/green]")

            # Start background tasks
            listener_task = asyncio.create_task(ws_listener(websocket))
            heartbeat_task = asyncio.create_task(heartbeat_loop(websocket))
            shell_task = asyncio.create_task(shell_loop(websocket))

            try:
                # Keep running until one of the tasks fails or finishes
                done, pending = await asyncio.wait(
                    [listener_task, heartbeat_task, shell_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )

                for task in pending:
                    task.cancel()

            except asyncio.CancelledError:
                console.print("\n[yellow]Disconnecting...[/yellow]")
            finally:
                if state.is_connected:
                    await websocket.close()
                    state.is_connected = False

    except Exception as e:
        console.print(f"[red]Failed to connect: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def connect(url: str = typer.Option(DEFAULT_URL, help="WebSocket URL of the server.")):
    """Establish a connection to the Nanocore server."""
    try:
        asyncio.run(run_client(url))
    except KeyboardInterrupt:
        pass


def main():
    app()


if __name__ == "__main__":
    main()
