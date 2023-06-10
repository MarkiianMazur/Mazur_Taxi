class Passenger:
    def __init__(self, id, name, total_cost):
        self.id = id
        self.name = name
        self.total_cost = total_cost


class Taxi:
    def __init__(self, id, model, position_x, position_y, available):
        self.id = id
        self.model = model
        self.position_x = position_x
        self.position_y = position_y
        self.available = available


class Order:
    def __init__(self, id, passenger_id, taxi_id, start_x, start_y, end_x, end_y, cost):
        self.id = id
        self.passenger_id = passenger_id
        self.taxi_id = taxi_id
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.cost = cost


class Offer:
    def __init__(self, id, distance_min, distance_max, cost):
        self.id = id
        self.distance_min = distance_min
        self.distance_max = distance_max
        self.cost = cost
