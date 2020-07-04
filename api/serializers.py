from flask_restplus import fields
from api.restplus import api


api_keys = api.model('Api keys', {
    'api_key': fields.String(required=True, readOnly=True, description='api key'),
    'app_version': fields.String(required=True, readOnly=True, description='app version'),
})

change_price = api.inherit('Change price', api_keys, {
    'user_id': fields.Integer(required=True, readOnly=True, description='user id'),
    'site_id': fields.Integer(required=True, readOnly=True, description='site id'),
    'variant_id': fields.Integer(required=True, readOnly=True, description='variant id'),
    'product_id': fields.Integer(required=True, readOnly=True, description='product id'),
    'min_price': fields.Integer(description='decrease price until'),
    'max_price': fields.Integer(description='increase price until')
})

user_model = api.inherit('user model', api_keys, {
    'phone_number': fields.String(required=True, readOnly=True, description='phone number'),
    'username': fields.String(readOnly=True, description='username'),
    'first_name': fields.String(readOnly=True, description='first name'),
    'last_name': fields.String(readOnly=True, description='last name')
})

favorite_model = api.inherit('favorite model', api_keys, {
    'user_id': fields.Integer(required=True, readOnly=True, description='user id'),
    'site_id': fields.Integer(required=True, readOnly=True, description='site id'),
    'category_id': fields.Integer(required=True, readOnly=True, description='category id'),
    'site_name': fields.String(readOnly=True, description='site name'),
    'product_name': fields.String(required=True, readOnly=True, description='product name'),
    'product_url': fields.String(required=True, readOnly=True, description='title fa'),
    'min_price': fields.Integer(readOnly=True, description='title fa'),
    'max_price': fields.Integer(readOnly=True, description='title fa'),
    'description': fields.String(readOnly=True, description='title en')
})

user_login = api.inherit('user login', api_keys, {
    'id': fields.Integer(readOnly=True, description='user id'),
    'phone_number': fields.String(required=True, readOnly=True, description='phone number'),
    'password': fields.String(required=True, readOnly=True, description='password')
})

user_profile = api.inherit('user profile', api_keys, {
    'id': fields.Integer(required=True, readOnly=True, description='user id'),
    'first_name': fields.String(readOnly=True, description='first name'),
    'last_name': fields.String(readOnly=True, description='last name'),
    'birthday': fields.String(readOnly=True, description='birthday'),
    'avatar': fields.String(readOnly=True, description='avatar'),
    'gender': fields.String(readOnly=True, description='gender enum female, male'),
    'birthday_access': fields.String(readOnly=True, description='birthday access enum public, friends, hidden')
})

profile = api.inherit('profile', api_keys, {
    'id': fields.Integer(required=True, readOnly=True, description='user id')
})

feature_model = api.model('feature model', {
    'name': fields.String(readOnly=True, description='feature name'),
    'value': fields.String(readOnly=True, description='value'),
    'active': fields.Boolean(readOnly=True, description='status')
})

related_user_model = api.model('related user model', {
    'user_id': fields.String(readOnly=True, description='user id'),
    'related_user_id': fields.String(readOnly=True, description='related user id')
})
