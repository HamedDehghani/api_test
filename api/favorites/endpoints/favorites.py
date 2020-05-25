import logging

from flask_restplus import Resource
from api.restplus import api
from api.serializers import favorite_model
from config import settings, status
from flask_jwt_extended import jwt_required
from entities.favorites import FavoriteModel

log = logging.getLogger(__name__)
ns = api.namespace('favorite', description='Operations related to favorites')


@ns.route('/list')
class FavoriteCollection(Resource):
    @api.marshal_with(favorite_model, as_list=True)
    @jwt_required
    def post(self):
        """
        Returns list of products.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        favorites = FavoriteModel()
        return favorites.get_all()
