import logging
import time
import os


log_file = "dataManager.log"
try:
    open(log_file, 'w').close()
except:
    pass
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=log_file, level=logging.DEBUG)
logging.disable(logging.DEBUG)
logging.info("Starting log at " + time.ctime() + "...")

user = "user"
password = "password"
host = "127.0.0.1"
port = "5432"
database = "hfd"

channels=["book.BTC-PERPETUAL.100ms"]
