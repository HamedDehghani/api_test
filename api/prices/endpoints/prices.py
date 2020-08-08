import logging

from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from api.restplus import api
from api.serializers import change_price
from config import settings, status
from entities.variant_price import VariantPriceModel

log = logging.getLogger(__name__)
ns = api.namespace('prices', description='Operations related to prices')


@ns.route('/change_price')
class FeaturesCollection(Resource):
    @api.marshal_with(change_price)
    @jwt_required
    def post(self):
        """
        Returns list of prices.
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED
        variant_prices = VariantPriceModel()
        variant_prices.deserialize(api.payload)

        return variant_prices.get_all()
