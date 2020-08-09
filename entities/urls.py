import json
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from app import db


class UrlModel(db.Model):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), unique=True, nullable=True)
    site_id = Column(Integer, ForeignKey('sites.id'), nullable=False)
    description = Column(String(120), unique=True, nullable=True)
    active = Column(Boolean, nullable=False)
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
        result = db.session.query(UrlModel).all()
        return result

    @staticmethod
    def find_by_site_id(site_id):
        result = db.session.query(UrlModel).filter(UrlModel.site_id == site_id).first()
        return result

    @staticmethod
    def deactive(id, user_id):
        url_model = db.session.query(UrlModel).filter(UrlModel.id == id, UrlModel.active).first()
        url_model.updated_at = datetime.now()
        url_model.active = False
        try:
            UrlModel.add(url_model)
            return {
                'message': 'url {0} deactive from user {1}.'.format(url_model.id, user_id),
                'id': url_model.id
            }
        except Exception as e:
            return {'message': str(e)}
