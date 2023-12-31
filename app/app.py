#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Routes
@app.route('/')
def home():
    return 'This is working'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict())
    else:
        response = make_response(
            jsonify({"error": "Hero not found"}),
            404
        )
        return response

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    else:
        response = make_response(
            jsonify({"error": "Power not found"}),
            404
        )
        return response

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    data = request.get_json()
    power = Power.query.get(id)

    if power:
        power.description = data.get('description', power.description)

        try:
            db.session.commit()
            return jsonify(power.to_dict())
        except Exception as e:
            db.session.rollback()
            response = make_response(
                jsonify({"errors": [str(e)]}),
                400
            )
            return response
    else:
        response = make_response(
            jsonify({"error": "Power not found"}),
            404
        )
        return response

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    new_hero_power = HeroPower(
        strength=data.get('strength'),
        hero_id=data.get('hero_id'),
        power_id=data.get('power_id')
    )

    try:
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify(new_hero_power.hero.to_dict())
    except Exception as e:
        db.session.rollback()
        response = make_response(
            jsonify({"errors": [str(e)]}),
            400
        )
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
