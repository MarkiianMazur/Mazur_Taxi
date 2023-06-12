from config import DB_CONFIG
from peewee import PostgresqlDatabase


class Connection:
    def __init__(self):
        self.database = PostgresqlDatabase(**DB_CONFIG)

    def get_database(self):
        return self.database
