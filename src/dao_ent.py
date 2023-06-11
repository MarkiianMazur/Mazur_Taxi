class PassengerDAO:
    def create(self, client):
        pass

    def read(self, client_id):
        pass


class TaxiDAO:
    def create(self, taxi):
        pass

    def get_models(self):
        pass

    def get_nearest_available_taxi(self, start_x, start_y, model):
        pass

    def update(self, taxi):
        pass

    def read(self, taxi_id):
        pass


class OrderDAO:
    def create(self, order):
        pass

    def read(self, order_id):
        pass


class OfferDAO:
    def create(self, offer):
        pass

    def get_offer_or_none(self, distance):
        pass

    def read(self, offer_id):
        pass
