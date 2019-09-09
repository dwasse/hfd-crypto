import asyncio
import websockets
import json
import ast
import logging
import time


class DeribitWebsocket:

    def __init__(self, message_callback=None):
        self.channels = []
        self.message_callback = message_callback
        self.url = 'wss://www.deribit.com/ws/api/v2'
        self._shutdown = False

    def _on_message(self, message):
        if self.message_callback is not None:
            self.message_callback(message)
        else:
            logging.info("Received message: " + str(message))

    def shutdown(self):
        self._shutdown = True

    def is_shutdown(self):
        return self._shutdown

    def connect(self, channels=None):
        if channels is not None:
            self.channels = channels
        msg = {
            "jsonrpc": "2.0",
            "method": "public/subscribe",
            "id": 42,
            "params": {
                "channels": self.channels
            }
        }

        async def call_api(msg):
            async with websockets.connect(self.url) as websocket:
                await websocket.send(msg)
                while websocket.open and not self._shutdown:
                    response = await websocket.recv()
                    self._on_message(response)
                logging.info("Deribit websocket closed at " + time.ctime())
        asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))

