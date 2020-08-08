import logging

from api.restplus import api
from api.serializers import favorite_list_model, favorite_list_add_model, favorite_list_deactive_model, \
    favorite_list_item_model
from config import settings, status
from datetime import datetime

from entities.favorite_list_items import FavoriteListItemModel
from entities.favorite_list import FavoriteListModel
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

log = logging.getLogger(__name__)
ns = api.namespace('favorite_list', description='Operations related to favorite list')


@ns.route('/list')
class FavoriteListCollection(Resource):
    @api.marshal_with(favorite_list_model, as_list=True)
    @jwt_required
    def post(self):
        """
        Returns list of favorite list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED
        user_id = api.payload.get('user_id')
        favorite_list = FavoriteListModel()
        return favorite_list.get_by_user_id(user_id)


@ns.route('/add')
class FavoriteListAdd(Resource):
    @api.expect(favorite_list_add_model, validate=True)
    @jwt_required
    def put(self):
        """
        add new favorite list.
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = FavoriteListModel()
        entity.deserialize(api.payload)
        entity.active = True
        entity.updated_at = datetime.now()
        try:
            FavoriteListModel.add(entity)
            return {
                'message': 'list {} added to favorite list.'.format(entity.name),
                'id': entity.id
            }
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/remove')
class FavoriteListRemove(Resource):
    @api.expect(favorite_list_deactive_model, validate=True)
    @jwt_required
    def post(self):
        """
        remove a favorite list from list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = FavoriteListModel()
        entity.deserialize(api.payload)
        try:
            return FavoriteListModel.deactive(entity.id, entity.user_id)
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/add_item')
class FavoriteListItemAdd(Resource):
    @api.expect(favorite_list_item_model, validate=True)
    @jwt_required
    def put(self):
        """
        add new item to favorite list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = FavoriteListItemModel()
        entity.deserialize(api.payload)

        entity.updated_at = datetime.now()
        entity.active = True
        try:
            FavoriteListItemModel.add(entity)
            return {
                'message': 'item {} added to favorite list.'.format(entity.related_user_id),
                'id': entity.id
            }
        except Exception as e:
            return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/remove_item')
class FavoriteListItemRemove(Resource):
    @api.expect(favorite_list_item_model, validate=True)
    @jwt_required
    def post(self):
        """
        remove a item from favorite list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = FavoriteListItemModel()
        entity.deserialize(api.payload)
        try:
            if entity.related_user_id is not None and entity.related_user_id > 0:
                return FavoriteListItemModel.deactive(entity.user_id, entity.related_user_id)
            return {'message': 'related_user_id is required'}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
