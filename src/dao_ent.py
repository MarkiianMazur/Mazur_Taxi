from abc import ABC
from models import Passenger, Taxi, Order, Offer


class PassengerDAO(ABC):
    def create(self, passenger: Passenger):
        pass

    def read(self, passenger_id: int):
        pass


class TaxiDAO:
    def create(self, taxi: Taxi):
        pass

    def get_models(self):
        pass

    def get_nearest_available_taxi(self, start_x: float, start_y: float, model: str):
        pass

    def update(self, taxi: Taxi):
        pass

    def read(self, taxi_id: int):
        pass


class OrderDAO:
    def create(self, order: Order):
        pass

    def read(self, order_id: int):
        pass


class OfferDAO:
    def create(self, offer: Offer):
        pass

    def get_offer_or_none(self, distance: float):
        pass

    def read(self, offer_id: int):
        pass
