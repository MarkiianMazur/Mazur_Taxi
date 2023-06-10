from dao_ent import PassengerDAO, TaxiDAO
from entities import Passenger, Taxi
from connection_pool import ConnectionPool, psycopg2


class PostgreSQLPassengerDAO(PassengerDAO):
    def create(self, passenger):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Passenger (name) VALUES (%s) RETURNING id, total_cost", (passenger.name,))
            connection.commit()
            response = cursor.fetchall()
            passenger.id = response[0][0]
            passenger.total_cost = response[0][1]
            return passenger
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating a passenger", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)

    def read(self, client_id):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Passenger WHERE id = %s", (client_id,))
            client_data = cursor.fetchone()
            if client_data:
                client = Passenger(client_data[0], client_data[1], client_data[2])
                return client
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading a passenger", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)


class PostgreSQLTaxiDAO(TaxiDAO):
    def create(self, taxi):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Taxi (model, position_x, position_y) VALUES (%s, %s, %s) RETURNING id, "
                           "available", (taxi.model, taxi.position_x, taxi.position_y))
            connection.commit()
            response = cursor.fetchall()
            taxi.id = response[0][0]
            taxi.available = response[0][1]
            return taxi
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating a taxi", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)

    def get_nearest_available_taxi(self, start_x, start_y, model):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Taxi WHERE is_available = TRUE AND model = %s ORDER BY SQRT(POWER(%s - position_x, "
                "2) + POWER(%s -position_y, 2)) LIMIT 1", (model, start_x, start_y))
            taxi_data = cursor.fetchone()
            if taxi_data:
                taxi = Taxi(taxi_data[0], taxi_data[1], taxi_data[2], taxi_data[3], taxi_data[4])
                return taxi
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while getting the nearest available taxi", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)

    def read(self, taxi_id):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Taxi WHERE id = %s", (taxi_id,))
            taxi_data = cursor.fetchone()
            if taxi_data:
                taxi = Taxi(taxi_data[0], taxi_data[1], taxi_data[2], taxi_data[3], taxi_data[4])
                return taxi
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading a taxi", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)
