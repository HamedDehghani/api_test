import logging

from flask import jsonify
from flask_restplus import Resource
from api.restplus import api
from api.serializers import product

log = logging.getLogger(__name__)
ns = api.namespace('favorites', description='Operations related to favorites')


@ns.route('/products')
class FeaturesCollection(Resource):
    @api.marshal_with(product)
    def post(self):
        """
        Returns list of products.
        """
        return jsonify({})
