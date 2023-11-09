from shop import db
from shop.models.base import Basemodel, Base
from flask_sqlalchemy import Column, Integer, String, Float, ForeignKey

class Product(Basemodel, Base):
    __tablename__ = 'products'
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.String(60), db.ForeignKey('users.id'))

    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')
    orders = db.relationship('OrderItem', backref='product', lazy='dynamic')

    def __init__(self, name, description, price, seller_id):
        self.name = name
        self.description = description
        self.price = price
        self.seller_id = seller_id
