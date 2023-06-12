import peewee
from src.connection import Connection

connection = Connection()


class BaseModel(peewee.Model):
    class Meta:
        database = connection.get_database()


class Passenger(peewee.Model):
    name = peewee.CharField()
    total_cost = peewee.FloatField(default=0)

    class Meta:
        database = connection.get_database()


class Taxi(peewee.Model):
    model = peewee.CharField()
    position_x = peewee.FloatField()
    position_y = peewee.FloatField()
    ppk = peewee.FloatField(default=1)
    available = peewee.BooleanField(default=True)

    class Meta:
        database = connection.get_database()


class Order(peewee.Model):
    passenger_id = peewee.ForeignKeyField(Passenger, backref='orders')
    taxi_id = peewee.ForeignKeyField(Taxi, backref='orders')
    start_x = peewee.FloatField()
    start_y = peewee.FloatField()
    end_x = peewee.FloatField()
    end_y = peewee.FloatField()
    distance = peewee.FloatField()
    cost = peewee.FloatField()

    class Meta:
        database = connection.get_database()


class Offer(peewee.Model):
    distance_min = peewee.FloatField()
    distance_max = peewee.FloatField()
    percent = peewee.FloatField()

    class Meta:
        database = connection.get_database()
