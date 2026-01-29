import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from nanocore.broker import Broker
from nanocore.rpn_worker import RPNWorker
from nanocore.config import config
from nanocore.ws_manager import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Nanocore Broker...")
    broker = Broker()

    # Register default RPN worker for demo/testing
    calc_worker = RPNWorker()
    broker.register_worker("default_calc", calc_worker, groups=["math"])

    # We need to run the worker loops.
    # In a real app, these might be separate processes or tasks.
    # Here we create tasks for each worker.
    worker_tasks = []
    for worker_id, worker in broker._workers.items():
        task = asyncio.create_task(worker.run(), name=f"worker-{worker_id}")
        worker_tasks.append(task)

    broker.start()
    app.state.broker = broker
    app.state.worker_tasks = worker_tasks

    # Heartbeat setup
    manager = ConnectionManager()
    hb_task = asyncio.create_task(manager.heartbeat_loop(), name="heartbeat-loop")
    app.state.ws_manager = manager
    app.state.hb_task = hb_task

    yield

    # Shutdown
    logger.info("Shutting down Nanocore Broker and Heartbeat...")
    hb_task.cancel()
    broker.stop()

    # Wait for worker tasks to complete
    if worker_tasks:
        await asyncio.gather(*worker_tasks, return_exceptions=True)
    logger.info("All workers stopped.")


app = FastAPI(
    title="Nanocore API",
    description="Asynchronous Knowledge Base Engine",
    version="0.1.0",
    lifespan=lifespan,
    debug=config.debug,
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "workers": (
            len(app.state.broker._workers) if hasattr(app.state, "broker") else 0
        ),
        "connections": (
            len(app.state.ws_manager.active_connections)
            if hasattr(app.state, "ws_manager")
            else 0
        ),
    }


from nanocore.schema import validate_message, create_message


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    manager: ConnectionManager = app.state.ws_manager
    broker: Broker = app.state.broker
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Heartbeat check
            if isinstance(data, dict) and data.get("type") == "pong":
                manager.on_pong(websocket)
            elif validate_message(data):
                msg_type = data["header"]["msg_type"]

                # Handle catalog request directly
                if msg_type == "get_catalog":
                    logger.info("Generating service catalog")
                    catalog = broker.get_catalog()
                    response = create_message(
                        msg_type="catalog_response",
                        body=catalog,
                        sender="broker",
                        receiver=data["header"]["sender"],
                    )
                    await websocket.send_json(response)
                else:
                    # Dispatch other messages to workers
                    logger.info(f"Dispatching message from WS: {msg_type}")
                    broker.dispatch(data)
            else:
                logger.warning(f"Received invalid message format from WS: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WS Error: {e}")
        manager.disconnect(websocket)
