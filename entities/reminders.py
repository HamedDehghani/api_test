import json
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from app import db


class ReminderModel(db.Model):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(1024))
    event_date = Column(DateTime)
    description = Column(String(255))
    active = Column(Boolean)
    updated_at = Column(DateTime)

    def deserialize(self, payload):
        self.__dict__.update(payload)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_user_id(user_id):
        result = db.session.query(ReminderModel).filter(
            ReminderModel.user_id == user_id, ReminderModel.active).all()
        return result

    @staticmethod
    def deactive(id):
        reminder = db.session.query(ReminderModel).filter(
            ReminderModel.id == id, ReminderModel.active).first()
        reminder.updated_at = datetime.now()
        reminder.active = False
        try:
            ReminderModel.add(reminder)
            return {
                'message': 'reminder {} remove from reminder list.'.format(reminder.id),
                'id': reminder.id
            }
        except Exception as e:
            return {'message': str(e)}
