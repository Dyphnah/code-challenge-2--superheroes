from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import random

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    powers = db.relationship('HeroPower', back_populates='hero')

    def to_dict(self, seen=None):
        if seen is None:
            seen = set()

        if self in seen:
            return {
                'id': self.id,
                'name': self.name,
                'super_name': self.super_name,
                'powers': [{'id': power.id, 'strength': power.strength, 'power': power.power.to_dict()} for power in self.powers]
            }

        seen.add(self)
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'powers': [{'id': power.id, 'strength': power.strength, 'power': power.power.to_dict(seen)} for power in self.powers]
        }


class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)

    heroes = db.relationship('HeroPower', back_populates='power')

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError(
                'Description must be at least 20 characters long.')
        return description

    def to_dict(self, seen=None):
        if seen is None:
            seen = set()

        if self in seen:
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description
            }

        seen.add(self)
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))

    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            # Choose a valid strength if the randomly selected one is not valid
            strength = random.choice(valid_strengths)
        return strength

    def to_dict(self, seen=None):
        if seen is None:
            seen = set()

        if self in seen:
            return {
                'id': self.id,
                'strength': self.strength,
                'hero': {
                    'id': self.hero.id,
                    'name': self.hero.name,
                    'super_name': self.hero.super_name,
                    'powers': [power.to_dict() for power in self.hero.powers]
                },
                'power': {
                    'id': self.power.id,
                    'name': self.power.name,
                    'description': self.power.description
                }
            }

        seen.add(self)
        return {
            'id': self.id,
            'strength': self.strength,
            'hero': self.hero.to_dict(seen),
            'power': self.power.to_dict()
        }
