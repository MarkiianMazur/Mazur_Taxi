from flask import Flask, render_template, request, redirect, url_for
from models import *
from services import Services

app = Flask(__name__)

services = Services()


@app.get('/')
def index_get():
    models = services.get_taxi_models()
    return render_template('index.html', title='Taxi Service', models=models)


@app.post('/')
def index_post():
    passenger = Passenger(name=request.form['name'])
    passenger = services.create_passenger(passenger)
    taxi = services.get_nearest_taxi(start_x=float(request.form['sx']), start_y=float(request.form['sy']),
                                     model=request.form['model'])
    if taxi:
        travel_detail = services.travel(passenger.id, taxi.id, float(request.form['sx']), float(request.form['sy']),
                                        float(request.form['ex']), float(request.form['ey']))
        taxi.available = False
        services.update_taxi(taxi)
        order = Order(passenger.id, taxi.id, request.form['sx'], request.form['sy'], request.form['ex'],
                      request.form['ey'], travel_detail['distance'], travel_detail['price'])
        # order.save()
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
    taxi = services.get_taxi_by_id(int(request.form['t']))
    taxi.available = True
    services.update_taxi(taxi)
    return redirect(url_for('index_get'))
