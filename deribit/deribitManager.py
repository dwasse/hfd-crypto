import config
import logging
import json
from .deribitRest import DeribitRest
from .deribitWebsocket import DeribitWebsocket


class DeribitManager:

    def __init__(self, db=None):
        self.db = db
        logging.info("Initializing Deribit REST client...")
        self.rest = DeribitRest()
        logging.info("Initializing Deribit websocket...")
        self.websocket = DeribitWebsocket(message_callback=self._message_callback)
        self.instruments = self.rest.getinstruments()
        logging.info("Got instruments: " + str(self.instruments))

    def connect_websocket(self, instruments="all", interval=100, book=True, trades=True):
        if instruments == "all":
            instruments = [i['instrumentName'] for i in self.instruments]
        book_channels = []
        trade_channels = []
        if book:
            book_channels = ["book." + i + "." + str(interval) + "ms" for i in instruments]
        if trades:
            trade_channels = ["trades." + i + "." + str(interval) + "ms" for i in instruments]
        channels = book_channels + trade_channels
        print("Channels: " + str(channels))
        logging.info("Connecting Deribit websocket to channels: " + str(channels) + "...")
        self.websocket.connect(channels)

    def _message_callback(self, message):
        print("Message: " + str(message))
        message_json = json.loads(message)
        try:
            data = message_json['params']['data']
            channel = message_json['params']['channel']
            [channel_type, instrument, interval] = channel.split('.')
            if channel_type == "book":
                if data['type'] == "snapshot":
                    self.db.insert_json("OrderSnapshots", data)
                elif data['type'] == "change":
                    self.db.insert_order_update(data, instrument=instrument)
            elif channel_type == 'trades':
                self.db.insert_trade_update(data, instrument=instrument)

        except Exception as e:
            logging.error("Error parsing message: " + str(message) + ", exception: " + str(e))
        try:
            data = message_json['params']['data']
            channel = message_json['params']['channel']
            if "book" in channel:
                self.db.insert_json("Orders", data)
            elif "trades" in channel:
                self.db.insert_json("Trades", data)
        except Exception as e:
            logging.error("Error storing raw message: " + str(e))