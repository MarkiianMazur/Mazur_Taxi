from math import e

from dao_imp import PostgreSQLPassengerDAO, PostgreSQLTaxiDAO, PostgreSQLOrderDAO, PostgreSQLOfferDAO


def travel(passenger, taxi, start_x, start_y, end_x, end_y):
    # calculate distance from passenger to taxi
    distance = (start_x - end_x) ** 2 + (start_y - end_y) ** 2
    if distance != 0:
        distance = distance ** 0.5
    # get offers
    offer_dao = PostgreSQLOfferDAO()
    # offer for distance
    offer = offer_dao.get_offer_or_none(distance)
    # offer for passenger
    pas_offer = 20 - e ** (-float(passenger.total_cost)/666) * 20
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
