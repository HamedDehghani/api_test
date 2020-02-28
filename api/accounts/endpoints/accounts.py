import logging

from flask import jsonify
from flask_restplus import Resource
from api.restplus import api
from api.serializers import user_signup

log = logging.getLogger(__name__)
ns = api.namespace('account', description='Operations related to accounts')


@ns.route('/signup')
class FeaturesCollection(Resource):
    @api.marshal_with(user_signup)
    def post(self):
        """
        signup.
        """
        return jsonify({})
