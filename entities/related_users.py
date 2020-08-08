import json
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from app import db


class RelatedUserModel(db.Model):
    __tablename__ = 'related_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(db.Integer, ForeignKey('users.id'), nullable=False)
    related_user_id = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)
    created_at = Column(DateTime)
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
        result = db.session.query(RelatedUserModel).all()
        return result

    @staticmethod
    def get_by_user_id(user_id):
        result = db.session.query(RelatedUserModel).filter(RelatedUserModel.user_id == user_id).all()
        return result

    @staticmethod
    def deactive(user_id, related_user_id):
        related_user = db.session.query(RelatedUserModel).filter(
            RelatedUserModel.user_id == user_id,
            RelatedUserModel.related_user_id == related_user_id,
            RelatedUserModel.active).first()
        RelatedUserModel.updated_at = datetime.now()
        related_user.active = False
        try:
            RelatedUserModel.add(related_user)
            return {
                'message': 'user {} remove from related.'.format(related_user.related_user_id),
                'id': related_user.id
            }
        except Exception as e:
            return {'message': str(e)}
