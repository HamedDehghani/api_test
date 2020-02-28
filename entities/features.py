from sqlalchemy import Column, String, Integer, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from db_connector.postgresql_connector import engine
from sqlalchemy.orm import Session

Base = declarative_base()


class FeatureModel(Base):
    __tablename__ = 'features'
    id = Column(BigInteger)
    name = Column(String)
    value = Column(String)
    active = Column(Boolean)
    updated_at = Column(String)
    id = Column(Integer, primary_key=True)

    def __init__(self, name, value, active, updated_at):
        self.name = name
        self.value = value
        self.active = active
        self.updated_at = updated_at

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Features:

    def __init__(self):
        self.connection = engine.connect()
        self.session = Session(bind=self.connection)
        print("DB Instance created")

    def add(self, feature):
        self.connection.execute(f"""
            INSERT INTO features 
            (name, value, active, updated_at) VALUES(
            '{feature.name}', '{feature.value}', '{feature.active}',  '{feature.updated_at}')""")

    def fetch_all_features(self):
        result = self.session.query(FeatureModel).all()
        return result

    def fetch_by_query(self, query):
        result = self.connection.execute(f"SELECT * FROM {query}")

        for data in result.fetchall():
            print(data)
