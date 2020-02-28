from entities.variant_price import VariantPriceModel
from entities.features import Features


def get_prices():
    model = Features()
    features = model.fetch_all_features()
    results = []
    for item in features:
        results.append(VariantPriceModel.as_dict(item))
    return results
