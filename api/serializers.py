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

user_signup = api.inherit('user', api_keys, {
    'phone_number': fields.String(required=True, readOnly=True, description='phone_number')
})

product = api.inherit('Change price', api_keys, {
    'site_id': fields.Integer(required=True, readOnly=True, description='site id'),
    'site_name': fields.String(required=True, readOnly=True, description='site name'),
    'product_id': fields.Integer(required=True, readOnly=True, description='product id'),
    'title_fa': fields.String(description='title fa'),
    'title_en': fields.String(description='title en')
})
