from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from shop.models.base import Basemodel, Base
from shop import db


class Users(Basemodel, Base):
    __tablename__ = 'users'
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    avatar = db.Column(db.String(255), default=None)
    token = db.Column(db.String(255), default=None)
    password = db.Column(db.String(100), default=None)
    role = db.Column(db.String(30), default='GUEST')
    is_active = db.Column(db.Boolean, default=False)
    

    # Define the relationship through the association table
    cart = db.relationship('Cart', backref='user', uselist=False)
    products_for_sale = db.relationship('Product', backref='seller', lazy='dynamic')
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    def __init__(self, name, email, username, avatar=None, token=None, password=None, role='GUEST', is_active=False):
        self.name = name
        self.email = email
        self.username = username
        self.avatar = avatar
        self.token = token
        self.password = password
        self.role = role
        self.is_active = is_active
