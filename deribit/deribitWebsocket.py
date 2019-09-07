import asyncio
import websockets
import json
import ast
import logging


class DeribitWebsocket:

    def __init__(self, message_callback=None):
        self.channels = []
        self.message_callback = message_callback
        self.url = 'wss://www.deribit.com/ws/api/v2'

    def connect(self, channels):
        self.channels = []

        msg = {
            "jsonrpc": "2.0",
            "method": "public/subscribe",
            "id": 42,
            "params": {
                "channels": channels
            }
        }

        async def call_api(msg):
            async with websockets.connect(self.url) as websocket:
                await websocket.send(msg)
                while websocket.open:
                    response = await websocket.recv()
                    # do something with the notifications...
                    self._on_message(response)

        asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))

    def _on_message(self, message):
        print(message)
        if self.message_callback is not None:
            self.message_callback(message)
        else:
            logging.info("Received message: " + str(message))

