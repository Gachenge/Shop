from shop import db
from shop.models.base import Basemodel, Base
from sqlalchemy import Column, String

class Category(Basemodel, Base):
    __tablename__ = 'categories'
    name = db.Column(db.String(100), nullable=False, unique=True)

    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name