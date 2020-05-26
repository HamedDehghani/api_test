import logging

from flask_restplus import Resource
from api.restplus import api
from api.serializers import favorite_model
from config import settings, status
from flask_jwt_extended import jwt_required
from entities.favorites import FavoriteModel
from datetime import datetime

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


@ns.route('/add')
class FavoriteAdd(Resource):
    @api.expect(favorite_model, validate=True)
    @jwt_required
    def put(self):
        """
        add new product to favorite list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = FavoriteModel()
        entity.deserialize(api.payload)
        entity.updated_at = datetime.now()
        print(api.payload)
        try:
            FavoriteModel.add(entity)
            return {
                'message': 'product {} added to favorites.'.format(entity.product_name),
                'id': entity.id
            }
        except Exception as e:
            return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR
