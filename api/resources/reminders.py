import datetime
import json

import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import db
from api.database.models import Reminder

def _validate_field(data, field, proceed, errors, missing_okay=False):

    print(data[field])

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

def _reminder_payload(reminder):
    return {
      "data": {
        "type": "reminders",
        "id": reminder.id,
        "attributes": {
            "user_id": reminder.user_id,
            "location_reminder": null,
            "creation_date": reminder.creation_date,
            "schedule_reminder": null,
            "supplies": reminder.supplies,
            "show_supplies": reminder.show_supplies,
            "title": reminder.title
        }
      }
    }


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
        print(f'{reminder} POST reminders')
        if reminder is not None:
            reminder_payload = _reminder_payload(reminder)
            reminder_payload['success'] = True
            return reminder_payload, 201
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
        results = [_reminder_payload(reminder) for reminder in reminders]
        return {
            'success': True,
            'results': results
        }, 200


class ReminderResource(Resource):
    """
    this Resource file is for our /users endpoints which do require
    a resource ID in the URI path
    GET /users/6
    DELETE /users/3
    PATCH /users/18
    """
    def get(self, *args, **kwargs):
        reminder_id = int(bleach.clean(kwargs['reminder_id'].strip()))
        reminder = None
        try:
            reminder = db.session.query(Reminder).filter_by(id=reminder_id).one()
        except NoResultFound:
            return abort(404)

        reminder_payload = _reminder_payload(reminder)
        reminder_payload['success'] = True
        return reminder_payload, 200

    def patch(self, *args, **kwargs):
        reminder_id = int(bleach.clean(kwargs['reminder_id'].strip()))
        reminder = None
        try:
            reminder = db.session.query(Reminder).filter_by(id=reminder_id).one()
        except NoResultFound:
            return abort(404)

        proceed = True
        errors = []
        data = json.loads(request.data)
        proceed, title, errors = _validate_field(
            data, 'title', proceed, errors, missing_okay=True)
        proceed, supplies, errors = _validate_field(
                    data, 'supplies', proceed, errors)
        proceed, show_supplies, errors = _validate_field(
            data, 'show_supplies', proceed, errors)
        proceed, user_id, errors = _validate_field(
            data, 'user_id', proceed, errors)

        if not proceed:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400

        if title and len(title.strip()) > 0:
            reminder.title = title
        reminder.update()

        reminder_payload = _reminder_payload(reminder)
        reminder_payload['success'] = True
        return reminder_payload, 200

    def delete(self, *args, **kwargs):
        reminder_id = kwargs['reminder_id']
        reminder = None
        try:
            reminder = db.session.query(Reminder).filter_by(id=reminder_id).one()
        except NoResultFound:
            return abort(404)

        reminder.delete()
        return {}, 204

class UsersRemindersResource(Resource):
    def get(self, *args, **kwargs):
        reminders = Reminder.queryfilter_by(user_id=user_id).order_by(
            Reminder.id.asc()
        ).all()
        results = [_reminder_payload(reminder) for reminder in reminders]
        return {
            'success': True,
            'results': results
        }, 200
