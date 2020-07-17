import logging

from api.restplus import api
from api.serializers import related_user_model
from config import settings, status
from datetime import datetime
from entities.related_users import RelatedUserModel
from entities.users import UserModel
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from utils import common_tools

log = logging.getLogger(__name__)
ns = api.namespace('related_users', description='Operations related to favorites')


@ns.route('/list')
class RelatedCollection(Resource):
    @api.marshal_with(related_user_model, as_list=True)
    @jwt_required
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
class RelatedAdd(Resource):
    @api.expect(related_user_model, validate=True)
    @jwt_required
    def put(self):
        """
        add new user to related users.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        related_user_id = api.payload.get('related_user_id', None)
        related_user_phone_number = api.payload.get('related_user_phone_number', None)
        if related_user_id is None and related_user_phone_number is None:
            return {'message': 'user id or phone is required.'}, status.HTTP_400_BAD_REQUEST
        if related_user_phone_number:
            api.payload['related_user_id'] = UserModel.find_by_phone_number(
                common_tools.Common.standardize_phone_number(related_user_phone_number)).id

        entity = RelatedUserModel()
        entity.deserialize(api.payload)

        entity.updated_at = datetime.now()
        entity.created_at = datetime.now()
        entity.active = True
        try:
            RelatedUserModel.add(entity)
            return {
                'message': 'user {} added to related users.'.format(entity.related_user_id),
                'id': entity.id
            }
        except Exception as e:
            return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/remove')
class RelatedRemove(Resource):
    @api.expect(related_user_model, validate=True)
    @jwt_required
    def post(self):
        """
        remove a user from related list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = RelatedUserModel()
        entity.deserialize(api.payload)
        try:
            return RelatedUserModel.deactive(entity.user_id, entity.related_user_id)
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
