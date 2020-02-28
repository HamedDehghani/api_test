import logging

from flask import jsonify
from flask_restplus import Resource
from api.prices import business
from api.restplus import api
from api.serializers import change_price

log = logging.getLogger(__name__)
ns = api.namespace('prices', description='Operations related to application features')


@ns.route('/change_price')
class FeaturesCollection(Resource):
    @api.marshal_with(change_price)
    def post(self):
        """
        Returns list of prices.
        """
        features = list(business.get_prices())
        return jsonify(features)
