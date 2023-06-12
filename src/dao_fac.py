from dao_imp import PostgreSQLPassengerDAO, PostgreSQLTaxiDAO, PostgreSQLOrderDAO, PostgreSQLOfferDAO
from connection import get_database


class DaoFactory:
    def __init__(self):
        self.database = get_database()
        self.passenger_dao = PostgreSQLPassengerDAO(self.database)
        self.taxi_dao = PostgreSQLTaxiDAO(self.database)
        self.order_dao = PostgreSQLOrderDAO(self.database)
        self.offer_dao = PostgreSQLOfferDAO(self.database)

    def get_passenger_dao(self):
        return self.passenger_dao

    def get_taxi_dao(self):
        return self.taxi_dao

    def get_order_dao(self):
        return self.order_dao

    def get_offer_dao(self):
        return self.offer_dao
