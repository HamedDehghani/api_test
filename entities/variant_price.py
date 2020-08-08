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


class VariantPrice:

    def __init__(self):
        self.connection = engine.connect()
        self.session = Session(bind=self.connection)
        print("DB Instance created")

    def add(self, variant_price):
        self.connection.execute(f"""
            INSERT INTO variant_prices 
            (product_id, category_id, status, variant_id, color_id, warranty_id, seller_id, selling_price, rrp_price, 
            is_incredible, is_promotion, updated_at) VALUES(
            '{variant_price.product_id}', '{variant_price.category_id}', '{variant_price.status}', 
            '{variant_price.variant_id}', '{variant_price.color_id}', '{variant_price.warranty_id}', 
            '{variant_price.seller_id}', '{variant_price.selling_price}', '{variant_price.rrp_price}',
            '{variant_price.is_incredible}', '{variant_price.is_promotion}', '{variant_price.updated_at}')""")

    def fetch_by_product_id(self, p_id):
        result = self.session.query(VariantPriceModel).filter(VariantPriceModel.variant_id == p_id)
        return result

    def fetch_all_variant_prices(self):
        result = self.session.query(VariantPriceModel).all()
        return result

    def fetch_by_query(self, query):
        result = self.connection.execute(f"SELECT * FROM {query}")

        for data in result.fetchall():
            print(data)
