import config
import sys
import traceback
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
        while not self.websocket.is_shutdown():
            try:
                logging.info("Opening Deribit websocket connection...")
                self.websocket.connect(channels)
            except Exception as e:
                logging.error("Error connecting to Deribit websocket: " + str(e))
                type_, value_, traceback_ = sys.exc_info()
                logging.error('Type: ' + str(type_))
                logging.error('Value: ' + str(value_))
                logging.error('Traceback: ' + str(traceback.format_exc()))

    def _message_callback(self, message):
        print("Message: " + str(message))
        message_json = json.loads(message)
        try:
            if 'params' in message_json:
                data = message_json['params']['data']
                channel = message_json['params']['channel']
                [channel_type, instrument, interval] = channel.split('.')
                if channel_type == "book":
                    if data['type'] == "snapshot":
                        self.db.insert_json("OrderSnapshots", data)
                    elif data['type'] == "change":
                        self.db.insert_order_update(data, instrument=instrument)
                elif channel_type == 'trades':
                    self.db.insert_trade_update(data)
            else:
                logging.info("Received irregular message: " + str(message))
        except Exception as e:
            logging.error("Error parsing message: " + str(message) + ", exception: " + str(e))
            type_, value_, traceback_ = sys.exc_info()
            logging.error('Type: ' + str(type_))
            logging.error('Value: ' + str(value_))
            logging.error('Traceback: ' + str(traceback.format_exc()))
        try:
            if 'params' in message_json:
                data = message_json['params']['data']
                channel = message_json['params']['channel']
                if "book" in channel:
                    self.db.insert_json("Orders", data)
                elif "trades" in channel:
                    self.db.insert_json("Trades", data)
            else:
                logging.info("Received irregular message: " + str(message))
        except Exception as e:
            logging.error("Error storing raw message: " + str(e))
            type_, value_, traceback_ = sys.exc_info()
            logging.error('Type: ' + str(type_))
            logging.error('Value: ' + str(value_))
            logging.error('Traceback: ' + str(traceback.format_exc()))
