from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shop.models.base import Basemodel, Base
from shop import db

class CartItem(Basemodel, Base):
    __tablename__ = 'cart_item'
    cart_id = db.Column(db.String(60), db.ForeignKey('carts.id'))
    product_id = db.Column(db.String(60), db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, cart_id, product_id, quantity=1):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
