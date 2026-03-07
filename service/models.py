import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(Enum):
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4
    TOOLS = 5

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Decimal(10, 2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(db.Enum(Category), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name == name)