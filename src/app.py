from flask import Flask, render_template, request, redirect, url_for, flash
from entities import Passenger, Taxi, Order, Offer
from dao_imp import PostgreSQLPassengerDAO, PostgreSQLTaxiDAO, PostgreSQLOrderDAO, PostgreSQLOfferDAO
from services import travel

app = Flask(__name__)


@app.get('/')
def index_get():
    taxi_dao = PostgreSQLTaxiDAO()
    taxies = taxi_dao.get_models()
    return render_template('index.html', title='Taxi Service', taxies=taxies)


@app.post('/')
def index_post():
    print(request.form)
    passenger_dao = PostgreSQLPassengerDAO()
    passenger = Passenger(None, request.form['name'], None)
    passenger = passenger_dao.create(passenger)
    taxi_dao = PostgreSQLTaxiDAO()
    taxi = taxi_dao.get_nearest_available_taxi(request.form['sx'], request.form['sy'], request.form['model'])
    if taxi:
        travel_detail = travel(passenger, taxi, float(request.form['sx']), float(request.form['sy']),
                               float(request.form['ex']), float(request.form['ey']))
        taxi.available = False
        taxi_dao.update(taxi)
        order_dao = PostgreSQLOrderDAO()
        order = Order(None, passenger.id, taxi.id, request.form['sx'], request.form['sy'], request.form['ex'],
                      request.form['ey'], travel_detail['distance'], travel_detail['price'])
        order_dao.create(order)
        travel_detail['model'] = taxi.model
        travel_detail['name'] = passenger.name
        travel_detail['cost'] = passenger.total_cost
        travel_detail['start_x'] = request.form['sx']
        travel_detail['start_y'] = request.form['sy']
        travel_detail['end_x'] = request.form['ex']
        travel_detail['end_y'] = request.form['ey']
        travel_detail['taxi_id'] = taxi.id
        return render_template('order.html', title='Order', travel_detail=travel_detail)
    return redirect(url_for('order_get'))


@app.get('/order')
def order_get():
    return 'No available taxi!'


@app.post('/order')
def order_post():
    print(request.form)
    taxi_dao = PostgreSQLTaxiDAO()
    taxi = taxi_dao.read(request.form['t'])
    taxi.available = True
    taxi_dao.update(taxi)
    return redirect(url_for('index_get'))
