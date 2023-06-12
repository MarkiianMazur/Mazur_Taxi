from math import e
from connection import Connection
from dao_imp import PostgreSQLPassengerDAO, PostgreSQLTaxiDAO, PostgreSQLOrderDAO, PostgreSQLOfferDAO

connection = Connection()


class Services:
    def __init__(self):
        self.database = connection.get_database()
        self.passenger_dao = PostgreSQLPassengerDAO(self.database)
        self.taxi_dao = PostgreSQLTaxiDAO(self.database)
        self.order_dao = PostgreSQLOrderDAO(self.database)
        self.offer_dao = PostgreSQLOfferDAO(self.database)

    def create_passenger(self, passenger):
        passenger = self.passenger_dao.create(passenger)
        return passenger

    def create_order(self, order):
        order = self.order_dao.create(order)
        return order

    def travel(self, passenger, taxi, start_x, start_y, end_x, end_y):
        passenger = self.passenger_dao.read(passenger)
        taxi = self.taxi_dao.read(taxi)
        # calculate distance from passenger to taxi
        distance = (start_x - end_x) ** 2 + (start_y - end_y) ** 2
        if distance != 0:
            distance = distance ** 0.5
        # offer for distance
        offer = self.offer_dao.get_offer_or_none(distance)
        # offer for passenger
        pas_offer = 20 - e ** (-float(passenger.total_cost) / 666) * 20
        # calculate price
        price = distance * taxi.ppk * (1 - pas_offer / 100)
        result = {}
        if offer:
            price *= (1 - offer.percent / 100)
            result['offer'] = round(offer.percent, 0)
        else:
            result['offer'] = 0
        result['price'] = round(price, 2)
        result['distance'] = round(distance, 2)
        result['pas_offer'] = round(pas_offer, 0)
        result['ppk'] = taxi.ppk
        return result

    def get_nearest_taxi(self, start_x, start_y, model):
        taxi = self.taxi_dao.get_nearest_available_taxi(start_x, start_y, model)
        return taxi

    def get_taxi_models(self):
        models = self.taxi_dao.get_models()
        models = [model.model for model in models]
        return models

    def get_taxi_by_id(self, taxi_id):
        taxi = self.taxi_dao.read(taxi_id)
        return taxi

    def update_taxi(self, taxi):
        self.taxi_dao.update(taxi)
