import logging

from flask import jsonify
from flask_restplus import Resource
from api.features_flag.business import get_feature
from api.restplus import api

log = logging.getLogger(__name__)
ns = api.namespace('features', description='Operations related to application features')


@ns.route('/')
class FeaturesCollection(Resource):

    def post(self):
        """
        Returns list of application features.
        """
        features = list(get_feature())
        return jsonify(features)
