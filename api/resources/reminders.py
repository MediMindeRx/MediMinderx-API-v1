import datetime
import json

import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import db
from api.database.models import Reminder, RemindersSchema

reminders_schema = RemindersSchema(many=True)
reminder_schema = RemindersSchema()

def _validate_field(data, field, proceed, errors, missing_okay=False):

    if field in data:
        # sanitize the reminder input here
        data[field] = bleach.clean(data[field].strip())
        if len(data[field]) == 0:
            proceed = False
            errors.append(f"required '{field}' parameter is blank")
    if not missing_okay and field not in data:
        proceed = False
        errors.append(f"required '{field}' parameter is missing")
        data[field] = ''

    return proceed, data[field], errors


class RemindersResource(Resource):
    def _create_reminder(self, data):
        proceed = True
        errors = []

        proceed, title, errors = _validate_field(
            data, 'title', proceed, errors)
        proceed, supplies, errors = _validate_field(
            data, 'supplies', proceed, errors)
        proceed, show_supplies, errors = _validate_field(
            data, 'show_supplies', proceed, errors)
        proceed, user_id, errors = _validate_field(
            data, 'user_id', proceed, errors)

        if proceed:
            reminder = Reminder(
                title=title,
                supplies=supplies,
                show_supplies=show_supplies,
                user_id=user_id
            )
            db.session.add(reminder)
            db.session.commit()
            return reminder, errors
        else:
            return None, errors

    def post(self, *args, **kwargs):
        reminder, errors = self._create_reminder(json.loads(request.data))
        if reminder is not None:
            result = reminder_schema.dump(reminder)
            return result, 201
        else:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400

    def get(self, *args, **kwargs):
        reminders = Reminder.query.order_by(
            Reminder.id.asc()
        ).all()
        results = reminders_schema.dump(reminders)
        return results, 200

    def patch(self, *args, **kwargs):
        json_data = request.get_json(force=True)
        reminder_id = int(bleach.clean(json_data['id'].strip()))
        reminder = None
        try:
            reminder = Reminder.query.filter_by(id=json_data['id']).first()
        except NoResultFound:
            return abort(404)

        proceed = True
        errors = []
        data = json.loads(request.data)
        proceed, title, errors = _validate_field(
            data, 'title', proceed, errors, missing_okay=True)
        proceed, supplies, errors = _validate_field(
            data, 'supplies', proceed, errors, missing_okay=True)
        proceed, show_supplies, errors = _validate_field(
            data, 'show_supplies', proceed, errors, missing_okay=True)

        if not proceed:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400

        if title:
            reminder.title = title
        if supplies:
            reminder.supplies = supplies
        if show_supplies:
            reminder.show_supplies = show_supplies
        db.session.commit()

        result = reminder_schema.dump(reminder)
        return result, 200

    def delete(self, *args, **kwargs):
        json_data = request.get_json(force=True)
        reminder = None
        try:
            reminder = Reminder.query.filter_by(id=json_data['id']).first()
        except NoResultFound:
            return abort(404)

        reminder.delete()
        return {'message': 'Reminder successfully deleted'}, 200

class ReminderResource(Resource):
    def get(self, *args, **kwargs):
        reminder_id = int(bleach.clean(kwargs['reminder_id'].strip()))
        reminder = None
        try:
            reminder = db.session.query(Reminder).filter_by(id=reminder_id).one()
        except NoResultFound:
            return abort(404)

        result = reminder_schema.dump(reminder)
        return result, 200

class UsersRemindersResource(Resource):
    def get(self, *args, **kwargs):
        user_id = int(bleach.clean(kwargs['user_id'].strip()))
        reminders = Reminder.query.filter_by(user_id=user_id).order_by(
            Reminder.id.asc()
        ).all()
        results = reminders_schema.dump(reminders)
        return results, 200
