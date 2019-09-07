import config
import logging
from .deribitRest import DeribitRest
from .deribitWebsocket import DeribitWebsocket


class DeribitManager:

    def __init__(self, message_callback=None):
        logging.info("Initializing Deribit REST client...")
        self.rest = DeribitRest()
        logging.info("Initializing Deribit websocket...")
        self.websocket = DeribitWebsocket(message_callback=message_callback)
        self.instruments = self.rest.getinstruments()
        logging.info("Got instruments: " + str(self.instruments))

    def connect_websocket(self, instruments="all", interval=100, book=True, trades=True):
        if instruments == "all":
            instruments = [i['instrumentName'] for i in self.instruments]
        book_channels =  []
        trade_channels = []
        if book:
            book_channels = ["book." + i + "." + str(interval) + "ms" for i in instruments]
        if trades:
            trade_channels = ["trades." + i + "." + str(interval) + "ms" for i in instruments]
        channels = book_channels + trade_channels
        print("Channels: " + str(channels))
        logging.info("Connecting Deribit websocket to channels: " + str(channels) + "...")
        self.websocket.connect(channels)
