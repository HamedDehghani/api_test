import json

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from app import db


class FavoriteModel(db.Model):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    site_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    product_name = Column(String(255))
    product_url = Column(String(1024))
    image_url = Column(String(1024))
    description = Column(String(255))
    active = Column(Boolean)
    order = Column(Integer, nullable=True)
    min_price = Column(Integer, nullable=True)
    max_price = Column(Integer, nullable=True)
    expire_date = Column(DateTime)
    updated_at = Column(DateTime)

    def deserialize(self, payload):
        self.__dict__.update(payload)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        result = db.session.query(FavoriteModel).all()
        return result
