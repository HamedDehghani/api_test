import logging

from flask_restplus import Resource
from api.restplus import api
from api.serializers import related_user_model
from config import settings, status
from flask_jwt_extended import jwt_required
from entities.related_users import RelatedUserModel
from datetime import datetime

log = logging.getLogger(__name__)
ns = api.namespace('related_users', description='Operations related to favorites')


@ns.route('/list')
class FavoriteCollection(Resource):
    @api.marshal_with(related_user_model, as_list=True)
    # @jwt_required
    def post(self):
        """
        Returns list of related users.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED
        user_id = api.payload.get('user_id')
        related_users = RelatedUserModel()
        return related_users.get_by_user_id(user_id)


@ns.route('/add')
class FavoriteAdd(Resource):
    @api.expect(related_user_model, validate=True)
    @jwt_required
    def put(self):
        """
        add new user to related users.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = RelatedUserModel()
        entity.deserialize(api.payload)
        entity.updated_at = datetime.now()
        entity.created_at = datetime.now()
        entity.active = True
        try:
            RelatedUserModel.add(entity)
            return {
                'message': 'user {} added to related users.'.format(entity.id),
                'id': entity.id
            }
        except Exception as e:
            return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR
