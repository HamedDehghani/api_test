import logging

from flask_restplus import Resource
from api.restplus import api
from api.serializers import feature_model
from config import settings, status
from entities.features import FeatureModel

log = logging.getLogger(__name__)
ns = api.namespace('feature', description='Operations related to application features')


@ns.route('/list')
class FeaturesCollection(Resource):
    @api.marshal_with(feature_model, as_list=True)
    def post(self):
        """
        Returns list of application features.
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        features = FeatureModel()
        return features.get_all()
