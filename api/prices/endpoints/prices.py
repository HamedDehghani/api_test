import logging
from datetime import datetime

from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from api.restplus import api
from api.serializers import change_price, url_model, url_deactive_model
from config import settings, status
from entities.urls import UrlModel
from entities.variant_price import VariantPriceModel

log = logging.getLogger(__name__)
ns = api.namespace('prices', description='Operations related to prices')


@ns.route('/change_price')
class FeaturesCollection(Resource):
    @api.marshal_with(change_price)
    @jwt_required
    def post(self):
        """
        Returns list of prices.
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED
        variant_prices = VariantPriceModel()
        variant_prices.deserialize(api.payload)

        return variant_prices.get_all()


@ns.route('/add_url')
class SetNewUrl(Resource):
    @api.expect(url_model, validate=True)
    @jwt_required
    def put(self):
        """
        add new url.
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = UrlModel()
        entity.deserialize(api.payload)
        entity.active = True
        entity.updated_at = datetime.now()
        try:
            UrlModel.add(entity)
            return {
                'message': 'reminder {} added to reminders.'.format(entity.name),
                'id': entity.id
            }
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/remove_url')
class DeactiveUrl(Resource):
    @api.expect(url_deactive_model, validate=True)
    @jwt_required
    def post(self):
        """
        deactive a reminder from url list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = UrlModel()
        entity.deserialize(api.payload)
        try:
            return UrlModel.deactive(entity.id, entity.user_id)
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
