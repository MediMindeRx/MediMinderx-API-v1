import datetime
import json

import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import db
from api.database.models import Schedule, Reminder


def _validate_field(data, field, proceed, errors, missing_okay=False):
    if field in data:
        # sanitize the user input here
        data[field] = bleach.clean(data[field].strip())
        if len(data[field]) == 0:
            proceed = False
            errors.append(f"required '{field}' parameter is blank")
    if not missing_okay and field not in data:
        proceed = False
        errors.append(f"required '{field}' parameter is missing")
        data[field] = ''

    return proceed, data[field], errors


def _schedule_payload(schedule):
    return {
        'id': schedule.id,
        'schedule_name': schedule.schedule_name,
        'unix_time': schedule.unix_time,
        'days': schedule.days,
        'times': schedule.times
    }


class SchedulesResource(Resource):
    def _create_schedule(self, data):
        proceed = True
        errors = []

        proceed, schedule_name, errors = _validate_field(
            data, 'schedule_name', proceed, errors)
        proceed, unix_time, errors = _validate_field(
            data, 'unix_time', proceed, errors)
        proceed, days, errors = _validate_field(
            data, 'days', proceed, errors)
        proceed, times, errors = _validate_field(
            data, 'times', proceed, errors)

        if proceed:
            schedule = Schedule(
                schedule_name=schedule_name,
                unix_time=unix_time,
                times=times,
                days = days
            )
            db.session.add(schedule)
            db.session.commit()
            last_schedule = db.session.query(Schedule).order_by(Schedule.id.desc()).first()
            reminder = Reminder.query.filter_by(id=reminder_id).first()
            reminder.schedule_id = schedule.id
            reminder.update()
            return schedule, errors
        else:
            return None, errors

    def post(self, *args, **kwargs):
        schedule, errors = self._create_schedule(json.loads(request.data))

        if schedule is not None:
            schedule_payload = _schedule_payload(schedule)
            schedule_payload['success'] = True
            return schedule_payload, 201
        else:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400
