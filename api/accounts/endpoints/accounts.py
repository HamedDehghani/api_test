import logging

from flask_restplus import Resource
from datetime import datetime
from api.restplus import api
from api.serializers import user_login, user_model, user_profile
from config import settings, status
from entities.users import UserModel, RevokedTokenModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required
from flask_jwt_extended import get_jwt_identity, get_raw_jwt
import re
import random

log = logging.getLogger(__name__)
ns = api.namespace('account', description='Operations related to accounts')


def standardize_phone_number(mobile):
    valid_prefixes = '[+98|98|0098|09]'
    result = re.match('^' + valid_prefixes + '*([0-9]{10})$', mobile)
    if result:
        return '98' + result.group(1)
    else:
        return None


@ns.route('/registration')
class AccountRegistration(Resource):
    @api.expect(user_model, validate=True)
    def put(self):
        """
        account registration
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        user_model = UserModel()
        user_model.deserialize(api.payload)

        current_user = UserModel.find_by_phone_number(standardize_phone_number(user_model.phone_number))
        if current_user:
            token = random.randint(10001, 99999)
            current_user.password = UserModel.generate_hash(str(token))
            current_user.updated_at = datetime.now()
            try:
                UserModel.add(current_user)
                return {
                    'message': 'User {} already exists'.format(current_user.phone_number),
                    'token': token
                }
            except Exception as e:
                return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR

        user_model.password = UserModel.generate_hash(user_model.password)
        user_model.active = True
        user_model.updated_at = datetime.now()
        try:
            UserModel.add(user_model)

            return {
                'message': 'User {} was created'.format(user_model.username),
                'access_token': create_access_token(identity=user_model.username),
                'refresh_token': create_refresh_token(identity=user_model.username)
            }
        except Exception as e:
            return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/login')
class AccountLogin(Resource):
    @api.expect(user_login, validate=True)
    def post(self):
        """
        login
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        phone_number = api.payload['phone_number']
        current_user = UserModel.find_by_phone_number(phone_number)
        if not current_user:
            return {'message': 'User {} doesnt exist'.format(phone_number)}

        if UserModel.verify_hash(api.payload['password'], current_user.password):
            access_token = create_access_token(identity=phone_number)
            refresh_token = create_refresh_token(identity=phone_number)
            return {
                'message': 'Logged in as {}'.format(current_user.phone_number),
                'user_id': current_user.id,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


@ns.route('/logout')
class UserLogoutAccess(Resource):
    @api.expect(user_model, validate=True)
    @jwt_required
    def post(self):
        """
            logout
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except Exception as e:
            return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/profile')
class Profile(Resource):
    @api.expect(user_profile, validate=True)
    @jwt_required
    def put(self):
        """
        user profile
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        phone_number = api.payload.get('phone_number')
        current_user = UserModel.find_by_phone_number(standardize_phone_number(phone_number))
        if not current_user:
            return {'message': 'User {} doesnt exist'.format(phone_number)}

        current_user.first_name = api.payload.get('first_name')
        current_user.last_name = api.payload.get('last_name')
        current_user.birthday = api.payload.get('birthday')
        current_user.updated_at = datetime.now()
        try:
            UserModel.add(current_user)
            return {
                'message': 'User {} profile updated'.format(current_user.phone_number),
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'birthday': current_user.birthday
            }
        except Exception as e:
            return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/users')
class AccountRegistration(Resource):
    @api.marshal_with(user_model, as_list=True)
    @jwt_required
    def post(self):
        """
        user list
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        user_model = UserModel()
        return user_model.get_all()


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except Exception as e:
            return {'message': e}, status.HTTP_500_INTERNAL_SERVER_ERROR


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}