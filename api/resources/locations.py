import datetime
import json

import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import db
from api.database.models import Location, Reminder


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


def _location_payload(location):
    return {
        'id': location.id,
        'location_name': location.location_name,
        'longitude': location.longitude,
        'latitude': location.latitude
    }


class LocationsResource(Resource):
    def _create_location(self, data):
        proceed = True
        errors = []

        proceed, location_name, errors = _validate_field(
            data, 'location_name', proceed, errors)
        proceed, longitute, errors = _validate_field(
            data, 'longitute', proceed, errors)
        proceed, latitude, errors = _validate_field(
            data, 'latitude', proceed, errors)

        if proceed:
            location = Location(
                location_name=location_name,
                longitude=longitude,
                latitude = latitude
            )
            db.session.add(location)
            db.session.commit()
            return location, errors
        else:
            return None, errors

    def post(self, *args, **kwargs):
        location, errors = self._create_location(json.loads(request.data))
        last_location = db.session.query(Location).order_by(Location.id.desc()).first()
        reminder = Reminder.query.filter_by(id=reminder_id).first()
        reminder.location_id = location.id
        reminder.update()

        if location is not None:
            location_payload = _location_payload(location)
            location_payload['success'] = True
            return location_payload, 201
        else:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400
