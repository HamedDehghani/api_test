import json

from sqlalchemy import Column, String, Integer, Boolean
from app import db


class FeatureModel(db.Model):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    value = Column(String)
    active = Column(Boolean)
    updated_at = Column(String)

    def deserialize(self, payload):
        self.__dict__.update(payload)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        result = db.session.query(FeatureModel).all()
        return result

    @staticmethod
    def fetch_by_query(self, query):
        result = self.connection.execute(f"SELECT * FROM {query}")

        for data in result.fetchall():
            print(data)
