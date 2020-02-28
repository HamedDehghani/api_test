from flask_restplus import fields
from api.restplus import api

api_keys = api.model('Api keys', {
    'api_key': fields.String(required=True, readOnly=True, description='api key'),
    'user_id': fields.Integer(required=True, readOnly=True, description='user id'),
    'app_version': fields.String(required=True, readOnly=True, description='app version'),
})

change_price = api.inherit('Change price', api_keys, {
    'site_id': fields.Integer(required=True, readOnly=True, description='site id'),
    'variant_id': fields.Integer(required=True, readOnly=True, description='variant id'),
    'product_id': fields.Integer(required=True, readOnly=True, description='product id'),
    'min_price': fields.Integer(description='decrease price until'),
    'max_price': fields.Integer(description='increase price until')
})
