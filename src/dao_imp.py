from dao_ent import PassengerDAO, TaxiDAO, OrderDAO, OfferDAO
from entities import Passenger, Taxi, Order, Offer
from connection_pool import ConnectionPool, psycopg2


class PostgreSQLPassengerDAO(PassengerDAO):
    def create(self, passenger):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            # check if passenger with such name already exists
            cursor.execute("SELECT * FROM Passenger WHERE name = %s", (passenger.name,))
            response = cursor.fetchall()
            if not response:
                cursor.execute("INSERT INTO Passenger (name) VALUES (%s) RETURNING id, name, total_cost",
                               (passenger.name,))
                response = cursor.fetchall()
            connection.commit()
            passenger.id = response[0][0]
            passenger.name = response[0][1]
            passenger.total_cost = response[0][2]
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
            cursor.execute("INSERT INTO Taxi (model, position_x, position_y, ppk, available) VALUES (%s, %s, "
                           "%s) RETURNING id, available", (taxi.model, taxi.position_x, taxi.position_y, taxi.ppk,
                                                           True))
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

    def get_models(self):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            # get models with id
            cursor.execute("SELECT DISTINCT model FROM Taxi")
            models = cursor.fetchall()
            return models
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while getting taxi models", error)
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
                "SELECT * FROM Taxi WHERE available = TRUE AND model = %s ORDER BY SQRT(POWER(%s - position_x, "
                "2) + POWER(%s -position_y, 2)) LIMIT 1", (model, start_x, start_y))
            taxi_data = cursor.fetchone()
            if taxi_data:
                taxi = Taxi(taxi_data[0], taxi_data[1], taxi_data[2], taxi_data[3], taxi_data[4], taxi_data[5])
                return taxi
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while getting the nearest available taxi", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)

    def update(self, taxi):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE Taxi SET model = %s, position_x = %s, position_y = %s, available = %s WHERE id "
                           "= %s", (taxi.model, taxi.position_x, taxi.position_y, taxi.available, taxi.id))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while updating a taxi", error)
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
                taxi = Taxi(taxi_data[0], taxi_data[1], taxi_data[2], taxi_data[3], taxi_data[4], taxi_data[5])
                return taxi
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading a taxi", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)


class PostgreSQLOrderDAO(OrderDAO):
    def create(self, order):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO "order" (passenger_id, taxi_id, start_x, start_y, end_x, end_y, distance, cost) VALUES ('
                '%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id', (order.passenger_id, order.taxi_id, order.start_x,
                                                                 order.start_y, order.end_x, order.end_y,
                                                                 order.distance, order.cost))
            connection.commit()
            response = cursor.fetchall()
            order.id = response[0][0]
            return order
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating an order", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)

    def read(self, order_id):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Order WHERE id = %s", (order_id,))
            order_data = cursor.fetchone()
            if order_data:
                order = Order(order_data[0], order_data[1], order_data[2], order_data[3], order_data[4], order_data[5],
                              order_data[6], order_data[7], order_data[8])
                return order
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading an order", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)


class PostgreSQLOfferDAO(OfferDAO):
    def create(self, offer):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Offer (distance_min, distance_max, percent) VALUES (%s, %s, %s) RETURNING id",
                (offer.distance_min, offer.distance_max, offer.percent))
            connection.commit()
            response = cursor.fetchall()
            offer.id = response[0][0]
            return offer
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating an offer", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)

    def get_offer_or_none(self, distance):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Offer WHERE distance_min <= %s AND distance_max >= %s", (distance, distance))
            offer_data = cursor.fetchone()
            if offer_data:
                offer = Offer(offer_data[0], offer_data[1], offer_data[2], offer_data[3])
                return offer
            else:
                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while getting an offer", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)

    def read(self, offer_id):
        connection = None
        cursor = None
        try:
            connection = ConnectionPool.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Offer WHERE id = %s", (offer_id,))
            offer_data = cursor.fetchone()
            if offer_data:
                offer = Offer(offer_data[0], offer_data[1], offer_data[2], offer_data[3])
                return offer
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while reading an offer", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                ConnectionPool.return_connection(connection)
