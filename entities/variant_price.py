import json

from sqlalchemy import Column, String, Integer, BigInteger, Boolean
from db_connector.postgresql_connector import engine
from sqlalchemy.orm import Session
from app import db


class VariantPriceModel(db.Model):
    __tablename__ = 'variant_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    category_id = Column(Integer)
    status = Column(String)
    variant_id = Column(Integer)
    color_id = Column(Integer)
    warranty_id = Column(Integer)
    seller_id = Column(Integer)
    selling_price = Column(BigInteger)
    rrp_price = Column(BigInteger)
    is_incredible = Column(Boolean)
    is_promotion = Column(Boolean)
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
        result = db.session.query(VariantPriceModel).all()
        return result

    @staticmethod
    def get_by_product_id(p_id):
        result = db.session.query(VariantPriceModel).filter(VariantPriceModel.variant_id == p_id)
        return result

    @staticmethod
    def get_all_variant_prices():
        result = db.session.query(VariantPriceModel).all()
        return result

    @staticmethod
    def get_by_query(query):
        result = db.connection.execute(f"SELECT * FROM {query}")

        for data in result.fetchall():
            print(data)
