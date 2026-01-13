import asyncio
import json
import logging
from functools import wraps
from typing import Any, Dict, Optional, Callable
import websockets

from . import trigger, objects
from . import exceptions
from . import notifications

__version__ = "0.1.0"
__author__ = "dngynq"
__email__ = "dngynq@gmail.com"


logger = logging.getLogger("mcmsmp")

class MinecraftManagementClient:
    def __init__(
            self,
            uri: str,
            secret: str,
            tls: bool = False
    ):
        self.uri = uri
        self.secret = secret
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.request_id = 0
        self.notification_handlers: Dict[str, Callable] = {}
        self._pending_responses: Dict[int, asyncio.Future] = {}
        self._running = False
        self._listen_task: Optional[asyncio.Task] = None

    async def connect(self):
        headers = {
            "Authorization": f"Bearer {self.secret}"
        }
        self.ws = await websockets.connect(
            self.uri,
            subprotocols=["jsonrpc"],
            additional_headers=headers
        )
        logger.info("Connected to MCM Protocol")
        self._running = True
        self._listen_task = asyncio.create_task(self._message_processor())

        schema = await self.rpc("rpc.discover")
        logger.debug("API schema received")
        return schema

    async def close(self):
        self._running = False
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass

        if self.ws:
            await self.ws.close()
            logger.info("Connection closed")

    async def _message_processor(self):
        while self._running and self.ws:
            try:
                message = await self.ws.recv()
                await self._process_message(message)

            except asyncio.CancelledError:
                break
            except websockets.exceptions.ConnectionClosed:
                logger.info("WebSocket connection closed")
                break
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                await asyncio.sleep(1)

    async def _process_message(self, message):
        try:
            if isinstance(message, bytes):
                message = message.decode('utf-8')
            data = json.loads(message)
            logger.debug(f"Processing message: {data}")

            if 'method' in data and 'params' in data:
                if 'id' not in data or data['id'] is None:
                    method = data['method']
                    params = data['params']
                    logger.info(f"Received notification: {method}")
                    await self._handle_notification(method, params)
                    return
            if 'id' in data and data['id'] is not None:
                await self._handle_response(data)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {message}, error: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def _handle_response(self, response):
        request_id = response['id']
        logger.debug(f"Handling response for request {request_id}")

        if request_id in self._pending_responses:
            future = self._pending_responses.pop(request_id)

            if 'error' in response and response['error'] is not None:
                error_data = response['error']
                if isinstance(error_data, dict):
                    error_msg = error_data.get('message', str(error_data))
                else:
                    error_msg = str(error_data)
                future.set_exception(ValueError(f"RPC Error: {error_msg}"))
            elif 'result' in response:
                future.set_result(response['result'])
            else:
                future.set_exception(ValueError("Invalid response format"))

    async def rpc(self, method: str, params: Any = None) -> Any:
        self.request_id += 1
        current_id = self.request_id
        future = asyncio.Future()
        self._pending_responses[current_id] = future
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": current_id,
            "params": params if params is not None else []
        }

        request_str = json.dumps(request)
        logger.debug(f"Sending RPC request: {method} (id: {current_id})")
        await self.ws.send(request_str)
        try:
            result = await asyncio.wait_for(future, timeout=30)
            return result
        except asyncio.TimeoutError:
            if current_id in self._pending_responses:
                del self._pending_responses[current_id]
            raise TimeoutError(f"RPC request timeout for method: {method}")
        finally:
            if current_id in self._pending_responses:
                del self._pending_responses[current_id]

    def on_notification(self, notification_class):
        def decorator(handler: Callable):
            @wraps(handler)
            async def wrapper(params):
                try:
                    data_instance = notification_class.create_from_params(params)
                    await handler(data_instance)
                except (AttributeError, NotImplementedError):
                    await handler(params)
                except Exception as e:
                    logger.error(f"Error processing {notification_class.identifier}: {e}")
                    logger.debug(f"Params: {params}")

            self.notification_handlers[notification_class.identifier] = wrapper
            return handler

        return decorator

    async def _handle_notification(self, method: str, params):

        logger.info(f"Handling notification: {method}, params: {params}")

        if method in self.notification_handlers:
            handler = self.notification_handlers[method]
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(params)
                else:
                    handler(params)
            except Exception as e:
                logger.error(f"Error in notification handler for {method}: {e}")
        else:
            logger.debug(f"No handler for notification: {method}")