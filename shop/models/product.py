from shop import db
from shop.models.base import Basemodel, Base
from sqlalchemy import Column, String, Float, ForeignKey, Integer

class Product(Basemodel, Base):
    __tablename__ = 'products'
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    copies = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    category_id = db.Column(db.String(60), db.ForeignKey('categories.id'))

    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')
    orders = db.relationship('OrderItem', backref='product', lazy='dynamic')

    def __init__(self, name, description, price, seller_id, category_id):
        self.name = name
        self.description = description
        self.price = price
        self.seller_id = seller_id
        self.category_id = category_id
