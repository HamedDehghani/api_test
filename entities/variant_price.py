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

    def __init__(self, product_id, category_id, status, variant_id, color_id, warranty_id, seller_id, selling_price,
                 rrp_price, is_incredible, is_promotion, updated_at):
        self.product_id = product_id
        self.category_id = category_id
        self.status = status
        self.variant_id = variant_id
        self.color_id = color_id
        self.warranty_id = warranty_id
        self.seller_id = seller_id
        self.selling_price = selling_price
        self.rrp_price = rrp_price
        self.is_incredible = is_incredible
        self.is_promotion = is_promotion
        self.updated_at = updated_at

    def __repr__(self):
        return """id='%s', product_id='%s', category_id='%s', status='%s', variant_id='%s', color_id='%s', warranty_id='%s', seller_id='%s', selling_price='%s', rrp_price='%s', is_incredible='%s', is_promotion='%s', updated_at='%s'
            """ % (
            self.id, self.product_id, self.category_id, self.status, self.variant_id, self.color_id, self.warranty_id,
            self.seller_id, self.selling_price, self.rrp_price, self.is_incredible, self.is_promotion, self.updated_at)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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
