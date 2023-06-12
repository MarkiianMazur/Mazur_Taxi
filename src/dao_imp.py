from peewee import fn
from dao_ent import PassengerDAO, TaxiDAO, OrderDAO, OfferDAO
from models import Passenger, Taxi, Order, Offer


class PostgreSQLPassengerDAO(PassengerDAO):
    def __init__(self, database):
        self.database = database

    def create(self, passenger):
        passenger = Passenger.create(name=passenger.name)
        return passenger

    def read(self, client_id):
        passenger_q = Passenger.select().where(Passenger.id == client_id)
        if passenger_q:
            passenger = passenger_q.get()
            return passenger


class PostgreSQLTaxiDAO(TaxiDAO):
    def __init__(self, db):
        self.db = db

    def create(self, taxi):
        taxi = Taxi.create(model=taxi.model, position_x=taxi.position_x, position_y=taxi.position_y, ppk=taxi.ppk,
                           available=True)
        return taxi

    def get_models(self):
        models = Taxi.select(Taxi.model).distinct()
        return models

    def get_nearest_available_taxi(self, start_x, start_y, model):
        taxi_q = Taxi.select().where(Taxi.available == True, Taxi.model == model).order_by(
            fn.SQRT(fn.POWER(start_x - Taxi.position_x, 2) + fn.POWER(start_y - Taxi.position_y, 2))).limit(1)
        if taxi_q:
            taxi = taxi_q.get()
            return taxi
        else:
            return None

    def update(self, taxi):
        taxi_q = Taxi.select().where(Taxi.id == taxi.id)
        if taxi_q:
            taxi_q.get().update(model=taxi.model, position_x=taxi.position_x, position_y=taxi.position_y,
                                available=taxi.available)

    def read(self, taxi_id):
        taxi_q = Taxi.select().where(Taxi.id == taxi_id)
        if taxi_q:
            taxi = taxi_q.get()
            return taxi


class PostgreSQLOrderDAO(OrderDAO):
    def __init__(self, db):
        self.db = db

    def create(self, order):
        order = Order.create(passenger_id=order.passenger_id, taxi_id=order.taxi_id, start_x=order.start_x,
                             start_y=order.start_y, end_x=order.end_x, end_y=order.end_y, distance=order.distance,
                             cost=order.cost)
        return order

    def read(self, order_id):
        order_q = Order.select().where(Order.id == order_id)
        if order_q:
            order = order_q.get()
            return order


class PostgreSQLOfferDAO(OfferDAO):
    def __init__(self, db):
        self.db = db

    def create(self, offer):
        offer = Offer.create(distance_min=offer.distance_min, distance_max=offer.distance_max,
                             percent=offer.percent)
        return offer

    def get_offer_or_none(self, distance):
        offer_q = Offer.select().where(Offer.distance_min <= distance, Offer.distance_max >= distance)
        if offer_q:
            offer = offer_q.get()
            return offer
        else:
            return None

    def read(self, offer_id):
        offer_q = Offer.select().where(Offer.id == offer_id)
        if offer_q:
            offer = offer_q.get()
            return offer
