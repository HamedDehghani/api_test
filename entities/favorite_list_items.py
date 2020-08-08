import json
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from app import db


class FavoriteListItemModel(db.Model):
    __tablename__ = 'favorite_list_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    favorite_id = Column(Integer, ForeignKey('favorites.id'), nullable=False)
    favorite_list_id = Column(Integer, ForeignKey('favorite_list.id'), nullable=False)
    active = Column(Boolean)
    updated_at = Column(DateTime)

    def deserialize(self, payload):
        self.__dict__.update(payload)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_list_id(list_id, user_id):
        result = db.session.query(FavoriteListItemModel).filter(
            FavoriteListItemModel.user_id == user_id,
            FavoriteListItemModel.favorite_list_id == list_id,
            FavoriteListItemModel, FavoriteListItemModel.active).all()
        return result

    @staticmethod
    def deactive(id):
        favorite_list = db.session.query(FavoriteListItemModel).filter(
            FavoriteListItemModel.id == id, FavoriteListItemModel.active).first()
        favorite_list.updated_at = datetime.now()
        favorite_list.active = False
        try:
            FavoriteListItemModel.add(favorite_list)
            return {
                'message': 'list {} remove from favorite list.'.format(favorite_list.id),
                'id': favorite_list.id
            }
        except Exception as e:
            return {'message': str(e)}
