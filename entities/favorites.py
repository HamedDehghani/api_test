import json

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from app import db
from datetime import datetime


class FavoriteModel(db.Model):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    site_id = Column(Integer, ForeignKey('sites.id'), nullable=False)
    category_id = Column(Integer, nullable=True)
    product_id = Column(Integer, nullable=False)
    product_url = Column(String(1024))
    image_url = Column(String(1024))
    description = Column(String(255))
    active = Column(Boolean)
    order = Column(Integer, nullable=True)
    min_price = Column(Integer, nullable=True)
    max_price = Column(Integer, nullable=True)
    expire_date = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = (UniqueConstraint('site_id', 'product_id', 'user_id',
                                       name='favorites_user_id_site_id_product_id_key'),)

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

    @staticmethod
    def get_by_user_id(user_id):
        result = db.session.query(FavoriteModel).filter(FavoriteModel.user_id == user_id, FavoriteModel.active).all()
        return result

    @staticmethod
    def deactive(user_id, site_id, product_id):
        favorite = db.session.query(FavoriteModel).filter(FavoriteModel.user_id == user_id,
                                                          FavoriteModel.site_id == site_id,
                                                          FavoriteModel.product_id == product_id,
                                                          FavoriteModel.active).first()
        favorite.updated_at = datetime.now()
        favorite.active = False
        try:
            FavoriteModel.add(favorite)
            return {
                'message': 'product {} remove from favorites.'.format(favorite.product_id),
                'id': favorite.id
            }
        except Exception as e:
            return {'message': str(e)}
