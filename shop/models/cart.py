from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shop.models.base import Basemodel, Base
from shop import db

class Cart(Basemodel, Base):
    __tablename__ = 'carts'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'))


    items = db.relationship('CartItem', backref='cart', lazy='dynamic')

    def __init__(self, user_id):
        self.user_id = user_id
