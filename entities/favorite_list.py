import json
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from app import db


class FavoriteListModel(db.Model):
    __tablename__ = 'favorite_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(1024))
    description = Column(String(255))
    active = Column(Boolean)
    order = Column(Integer, nullable=True)
    updated_at = Column(DateTime)

    def deserialize(self, payload):
        self.__dict__.update(payload)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_user_id(user_id):
        result = db.session.query(FavoriteListModel).filter(
            FavoriteListModel.user_id == user_id, FavoriteListModel.active).all()
        return result

    @staticmethod
    def deactive(id):
        favorite_list = db.session.query(FavoriteListModel).filter(
            FavoriteListModel.id == id, FavoriteListModel.active).first()
        favorite_list.updated_at = datetime.now()
        favorite_list.active = False
        try:
            FavoriteListModel.add(favorite_list)
            return {
                'message': 'list {} remove from favorite list.'.format(favorite_list.id),
                'id': favorite_list.id
            }
        except Exception as e:
            return {'message': str(e)}
