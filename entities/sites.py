import json

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from app import db


class SiteModel(db.Model):
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    site_name = Column(String(120), unique=True, nullable=True)
    base_url = Column(String(255), unique=True, nullable=True)
    active = Column(Boolean, nullable=False)
    updated_at = Column(DateTime)

    favorites = db.relationship('FavoriteModel', backref=db.backref('sites'), lazy=True)

    def deserialize(self, payload):
        self.__dict__.update(payload)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        result = db.session.query(SiteModel).all()
        return result

    @staticmethod
    def find_by_site_name(site_name):
        result = db.session.query(SiteModel).filter(SiteModel.site_name == site_name).first()
        return result
