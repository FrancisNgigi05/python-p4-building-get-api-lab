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

@app.route('/bakeries')
def bakeries():
    data = []

    goods = Bakery.query.all()

    for good in goods:
        data.append(good.to_dict())

    response = make_response(jsonify(data), 200)

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    data = []

    good = Bakery.query.filter(Bakery.id == id).first()

    data.append(good.to_dict())

    response  = make_response(jsonify(data), 200)

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

    data = [good.to_dict() for good in baked_goods]

    response = make_response(jsonify(data), 200)

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    backed_good = BakedGood.query.order_by(desc(BakedGood.price)).first()

    response = (jsonify(backed_good.to_dict()), 200)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
