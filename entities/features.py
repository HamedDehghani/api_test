from sqlalchemy import Column, String, Integer, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

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
