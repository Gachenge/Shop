from shop import db
from shop.models.base import Basemodel, Base
from flask_sqlalchemy import Integer, Column, ForeignKey, String

class Order(Basemodel, Base):
    __tablename__ = 'orders'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    status = db.Column(db.String(20), nullable=False)  # e.g., 'placed', 'shipped', 'delivered'

    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __init__(self, user_id, status):
        self.user_id = user_id
        self.status = status
