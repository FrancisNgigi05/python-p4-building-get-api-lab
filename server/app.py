#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# This endpoint will return a list of JSON objects for all backeries in the db
@app.route('/bakeries')
def bakeries():
    bakeries_available = []

    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        bakeries_available.append(bakery_dict)

    response = make_response(bakeries_available, 200)

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(bakery_dict, 200)
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    sorted_bakeries = []

    for bakery in BakedGood.query.order_by(BakedGood.price).all():
        bakery_dict = bakery.to_dict()
        sorted_bakeries.append(bakery_dict)
    
    response = make_response(sorted_bakeries, 200)

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive_baked = BakedGood.query.order_by(desc(BakedGood.price)).first()
    expensive_dict = expensive_baked.to_dict()
    response = make_response(expensive_dict, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)