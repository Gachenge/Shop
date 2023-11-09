from shop import db
from shop.models.base import Basemodel, Base
from flask_sqlalchemy import Column, String, ForeignKey

class OrderItem(Basemodel, Base):
    __tablename__ = 'order_items'
    order_id = db.Column(db.String(60), db.ForeignKey('orders.id'))
    product_id = db.Column(db.String(60), db.ForeignKey('products.id'))

    def __init__(self, order_id, product_id):
        self.order_id = order_id
        self.product_id = product_id
