import logging

from api.restplus import api
from api.serializers import reminder_model, reminder_remove_model
from config import settings, status
from datetime import datetime

from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from entities.reminders import ReminderModel

log = logging.getLogger(__name__)
ns = api.namespace('reminder', description='Operations related to reminders')


@ns.route('/list')
class ReminderCollection(Resource):
    @api.marshal_with(reminder_model, as_list=True)
    @jwt_required
    def post(self):
        """
        Returns list of reminders.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED
        user_id = api.payload.get('user_id')
        reminders = ReminderModel()
        return reminders.get_by_user_id(user_id)


@ns.route('/add')
class ReminderAdd(Resource):
    @api.expect(reminder_model, validate=True)
    @jwt_required
    def put(self):
        """
        add new reminder.
        """

        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = ReminderModel()
        entity.deserialize(api.payload)
        entity.active = True
        entity.updated_at = datetime.now()
        try:
            ReminderModel.add(entity)
            return {
                'message': 'reminder {} added to reminders.'.format(entity.name),
                'id': entity.id
            }
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR


@ns.route('/remove')
class ReminderRemove(Resource):
    @api.expect(reminder_remove_model, validate=True)
    @jwt_required
    def post(self):
        """
        remove a reminder from list.
        """
        if api.payload.get('api_key') != settings.API_KEY:
            return {'message': 'api key unauthorized'}, status.HTTP_401_UNAUTHORIZED

        entity = ReminderModel()
        entity.deserialize(api.payload)
        try:
            return ReminderModel.deactive(entity.id, entity.user_id)
        except Exception as e:
            return {'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
