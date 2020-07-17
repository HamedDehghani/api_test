import logging

from api.restplus import api
from api.serializers import favorite_model, favorite_deactive_model
from config import settings, status
from datetime import datetime
from entities.favorites import FavoriteModel
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
import re

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
        favorites.deserialize(api.payload)
        return favorites.get_by_user_id(favorites.user_id)


def get_product_id_from_url(product_url):
    print(product_url)
    product_id = int(re.findall('(?:dkp-)(\w+)', product_url)[0])
    return product_id


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
        entity.site_id = 1
        entity.active = True
        entity.product_id = get_product_id_from_url(entity.product_url)
        entity.updated_at = datetime.now()
        try:
            FavoriteModel.add(entity)
            return {
                'message': 'product {} added to favorites.'.format(entity.product_id),
                'id': entity.id
            }
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/remove')
class FavoriteAdd(Resource):
    @api.expect(favorite_deactive_model, validate=True)
    @jwt_required
    def post(self):
        """
        remove a product favorite from list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = FavoriteModel()
        entity.deserialize(api.payload)
        try:
            return FavoriteModel.deactive(entity.user_id, entity.site_id, entity.product_id)
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
