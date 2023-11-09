from uuid import uuid4
from datetime import datetime
from shop import db
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


def get_uuid():
    return uuid4().hex


Base = declarative_base()


class Basemodel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(60), primary_key=True, default=get_uuid, unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def formatted_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
