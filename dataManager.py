from databaseController import DatabaseController
from deribit.deribitManager import DeribitManager
import logging
import time
import config


print("Initializing db controller...")
databaseController = DatabaseController(reset=True)
print("Initializing Deribit manager...")
deribitManager = DeribitManager(db=databaseController)
deribitManager.connect_websocket()

while True:
    time.sleep(5)
    print("Still alive")
