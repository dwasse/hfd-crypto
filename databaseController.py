import psycopg2
import config


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
        cursor.execute(query)
        self.connection.commit()
        return cursor

    def insert_json(self, table, json_data):
        data_str = str(json_data).replace("'", '"')
        query = "INSERT INTO " + table + "(Data) VALUES ('" + data_str + "');"
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

    def reset_db(self):
        query = "DROP TABLE IF EXISTS Trades, Orders;"
        self.execute(query)
        self.setup_db()
