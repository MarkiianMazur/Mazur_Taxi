from connection_pool import ConnectionPool
from app import app


if __name__ == '__main__':
    ConnectionPool.get_connection()

    app.run()

    ConnectionPool.close_all_connections()
