from connection_pool import ConnectionPool
from dao_imp import PostgreSQLPassengerDAO, PostgreSQLTaxiDAO
from entities import Passenger, Taxi


if __name__ == '__main__':
    ConnectionPool.get_connection()

    passenger1 = Passenger(None, 'John Porter', None)
    passenger_dao = PostgreSQLPassengerDAO()
    passenger_dao.create(passenger1)

    passenger_id = passenger1.id
    retrieved_passenger = passenger_dao.read(passenger_id)
    if retrieved_passenger:
        print(f"Retrieved client: ID={retrieved_passenger.id}, Name={retrieved_passenger.name}")
    else:
        print("Client not found")

    taxi1 = Taxi(None, 'Toyota Camry', 0, 0, True)
    taxi_dao = PostgreSQLTaxiDAO()
    taxi_dao.create(taxi1)

    taxi_id = taxi1.id
    retrieved_taxi = taxi_dao.read(taxi_id)
    if retrieved_taxi:
        print(f"Retrieved taxi: ID={retrieved_taxi.id}, Model={retrieved_taxi.model}")
    else:
        print("Taxi not found")

    ConnectionPool.close_all_connections()
