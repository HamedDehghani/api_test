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
    'site_id': fields.Integer(required=False, readOnly=True, description='site id'),
    'category_id': fields.Integer(required=False, readOnly=True, description='category id'),
    'site_name': fields.String(readOnly=True, description='site name'),
    'product_id': fields.Integer(required=False, readOnly=True, description='product id'),
    'product_url': fields.String(required=True, readOnly=True, description='title fa'),
    'min_price': fields.Integer(readOnly=True, description='title fa'),
    'max_price': fields.Integer(readOnly=True, description='title fa'),
    'description': fields.String(readOnly=True, description='title en')
})

favorite_deactive_model = api.inherit('favorite model', api_keys, {
    'user_id': fields.Integer(required=True, readOnly=True, description='user id'),
    'site_id': fields.Integer(required=True, readOnly=True, description='site id'),
    'product_id': fields.Integer(required=True, readOnly=True, description='product id')
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

feature_model = api.inherit('feature model', api_keys, {
    'name': fields.String(readOnly=True, description='feature name'),
    'value': fields.String(readOnly=True, description='value'),
    'active': fields.Boolean(readOnly=True, description='status')
})

related_user_model = api.inherit('related user model', api_keys, {
    'user_id': fields.Integer(required=True, readOnly=True, description='user id'),
    'related_user_id': fields.Integer(readOnly=True, description='related user id'),
    'related_user_phone_number': fields.String(readOnly=True, description='related user phone number')
})

favorite_list_model = api.inherit('favorite list model', api_keys, {
    'user_id': fields.Integer(required=True, readOnly=True, description='user id')
})

favorite_list_add_model = api.inherit('favorite list add model', api_keys, {
    'user_id': fields.Integer(required=True, readOnly=True, description='user id'),
    'name': fields.String(readOnly=True, description='list name'),
    'description': fields.String(readOnly=True, description='description'),
    'active': fields.Boolean(readOnly=True, description='status'),
    'order': fields.Integer(readOnly=True, description='order')
})

favorite_list_deactive_model = api.inherit('favorite list model', api_keys, {
    'id': fields.Integer(required=True, readOnly=True, description='favorite list id'),
    'user_id': fields.Integer(required=True, readOnly=True, description='user id')
})

favorite_list_item_model = api.inherit('favorite list item model', api_keys, {
    'favorite_list_id': fields.Integer(required=True, readOnly=True, description='favorite list id'),
    'favorite_id': fields.Integer(required=True, readOnly=True, description='favorite item id'),
    'user_id': fields.Integer(required=True, readOnly=True, description='user id')
})

reminder_model = api.inherit('reminder model', api_keys, {
    'name': fields.String(required=True, readOnly=True, description='name'),
    'event_date': fields.DateTime(required=True, readOnly=True, description='event_date'),
    'description': fields.String(readOnly=True, description='description'),
    'user_id': fields.Integer(required=True, readOnly=True, description='user id')
})

reminder_remove_model = api.inherit('reminder remove model', api_keys, {
    'id': fields.Integer(required=True, readOnly=True, description='name'),
    'user_id': fields.Integer(required=True, readOnly=True, description='user id')
})

url_model = api.inherit('url model', api_keys, {
    'url': fields.String(required=True, readOnly=True, description='name'),
    'user_id': fields.Integer(required=True, readOnly=True, description='user id'),
    'product_id': fields.Integer(readOnly=True, description='description'),
    'site_id': fields.Integer(readOnly=True, description='description')
})

url_deactive_model = api.inherit('url model', api_keys, {
    'id': fields.Integer(required=True, readOnly=True, description='favorite list id'),
    'user_id': fields.Integer(required=True, readOnly=True, description='user id')
})
