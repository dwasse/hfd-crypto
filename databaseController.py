import psycopg2
import config
import logging
import sys
import traceback


def quote(msg):
    return "'" + msg + "'"


class DatabaseController:

    def __init__(self,
                 user=config.user,
                 password=config.password,
                 host=config.host,
                 port=config.port,
                 database=config.database,
                 reset=False):
        self.user = user
        self._password = password
        self._host = host
        self._port = port
        self.database = database
        self.connection = None
        self.connect()
        if reset:
            self.reset_db()
        else:
            self.setup_db()

    def connect(self):
        self.connection = psycopg2.connect(
            user=self.user,
            password=self._password,
            host=self._host,
            port=self._port,
            database=self.database)

    def execute(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logging.error("Error executing query: " + query)
            type_, value_, traceback_ = sys.exc_info()
            logging.error('Type: ' + str(type_))
            logging.error('Value: ' + str(value_))
            logging.error('Traceback: ' + str(traceback.format_exc()))
            self.connection.rollback()
        return cursor

    def insert_json(self, table, json_data):
        data_str = str(json_data).replace("'", '"')
        query = "INSERT INTO " + table + "(Data) VALUES ('" + data_str + "');"
        self.execute(query)
        logging.info("executed query: " + query)

    def insert_order_update(self, data, instrument=None):
        if instrument is None:
            instrument = data['instrument_name']
        timestamp = data['timestamp']
        for bid in data['bids']:
            query = '''INSERT INTO OrderUpdates(Symbol, Type, Price, Amount, Side, Timestamp)
            VALUES(%s, %s, %s, %s, %s, %s)''' % (quote(instrument), quote(bid[0]), quote(str(bid[1])),
                                                 quote(str(bid[2])), quote("buy"), quote(str(timestamp)))
            self.execute(query)
            logging.info("executed query: " + query)
        for ask in data['asks']:
            query = '''INSERT INTO OrderUpdates(Symbol, Type, Price, Amount, Side, Timestamp)
            VALUES(%s, %s, %s, %s, %s, %s)''' % (quote(instrument), quote(ask[0]), quote(str(ask[1])),
                                                 quote(str(ask[2])), quote("sell"), quote(str(timestamp)))
            self.execute(query)
            logging.info("executed query: " + query)

    def insert_trade_update(self, data):
        for trade in data:
            query = '''INSERT INTO TradeUpdates(TradeId, Symbol, Price, Amount, Side, Timestamp)
            VALUES(%s, %s, %s, %s, %s, %s)''' \
                    % (quote(str(trade['trade_id'])), quote(trade['instrument_name']), quote(str(trade['price'])),
                       quote(str(trade['amount'])), quote(trade['direction']), quote(str(trade['timestamp'])))
            logging.info("executed query: " + query)
            self.execute(query)

    def setup_db(self):
        query = '''CREATE TABLE IF NOT EXISTS Trades(
            Id serial PRIMARY KEY,
            Data jsonb NOT NULL);'''
        self.execute(query)
        query = '''CREATE TABLE IF NOT EXISTS Orders(
            Id serial PRIMARY KEY,
            Data jsonb NOT NULL);'''
        self.execute(query)
        query = '''CREATE TABLE IF NOT EXISTS OrderUpdates(
            Id serial PRIMARY KEY,
            Symbol varchar(50) NOT NULL,
            Type varchar(10) NOT NULL,
            Price double precision NOT NULL,
            Amount double precision NOT NULL,
            Side varchar(4) NOT NULL,
            Timestamp bigint NOT NULL);'''
        self.execute(query)
        query = '''CREATE TABLE IF NOT EXISTS TradeUpdates(
            Id serial PRIMARY KEY,
            TradeId bigint NOT NULL,
            Symbol varchar(50) NOT NULL,
            Price double precision NOT NULL,
            Amount double precision NOT NULL,
            Side varchar(4) NOT NULL,
            Timestamp bigint NOT NULL);'''
        self.execute(query)
        query = '''CREATE TABLE IF NOT EXISTS OrderSnapshots(
            Id serial PRIMARY KEY,
            Data jsonb NOT NULL);'''
        self.execute(query)

    def reset_db(self):
        query = "DROP TABLE IF EXISTS Trades, Orders, OrderUpdates, TradeUpdates, OrderSnapshots;"
        self.execute(query)
        self.setup_db()
