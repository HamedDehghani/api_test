from entities.variant_price import VariantPriceModel
from entities.features import FeatureModel


def get_prices():
    model = FeatureModel()
    features = model.fetch_all_features()
    results = []
    for item in features:
        results.append(VariantPriceModel.as_dict(item))
    return results
