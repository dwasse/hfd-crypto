from databaseController import DatabaseController
from deribit.deribitManager import DeribitManager
import logging
import time
import config


def process_message(message):
    #todo: parse trade/order and insert into relevant table
    table = "Orders"
    databaseController.insert_json(table, message)
    logging.info("Inserted message to " + table + ": " + str(message))


print("Initializing db controller...")
databaseController = DatabaseController(reset=True)
print("Initializing Deribit manager...")
deribitManager = DeribitManager(message_callback=process_message)
deribitManager.connect_websocket()

while True:
    time.sleep(5)
    print("Still alive")
