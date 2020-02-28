from db_connector import postgresql_connector
from entities.variant_price import VariantPriceModel


def get_variant_price():
    variant_price_model = postgresql_connector.VariantPrice()
    # variant_prices = variant_price_model.fetch_by_product_id(3968124)
    variant_prices = variant_price_model.fetch_all_variant_prices()
    results = []
    for item in variant_prices:
        results.append(VariantPriceModel.as_dict(item))
    return results


def get_feature():
    feature_model = postgresql_connector.Features()
    features = feature_model.fetch_all_features()
    results = []
    for item in features:
        results.append(VariantPriceModel.as_dict(item))
    return results