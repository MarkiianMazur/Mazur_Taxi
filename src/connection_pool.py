import psycopg2
from config import DB_CONFIG
from psycopg2 import pool


class ConnectionPool:
    __connection_pool = None

    @classmethod
    def get_connection(cls):
        if cls.__connection_pool is None:
            cls.__connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONFIG)
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        if cls.__connection_pool is not None:
            cls.__connection_pool.closeall()
