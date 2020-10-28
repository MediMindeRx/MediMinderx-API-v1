import datetime
import json

import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import db
from api.database.models import Location, Reminder, LocationsSchema

locations_schema = LocationsSchema(many=True)
location_schema = LocationsSchema()


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


class LocationsResource(Resource):
    def _create_location(self, data):
        proceed = True
        errors = []

        proceed, location_name, errors = _validate_field(
            data, 'location_name', proceed, errors)
        proceed, longitude, errors = _validate_field(
            data, 'longitude', proceed, errors)
        proceed, latitude, errors = _validate_field(
            data, 'latitude', proceed, errors)
        proceed, address, errors = _validate_field(
            data, 'address', proceed, errors)
        proceed, reminder_id, errors = _validate_field(
            data, 'reminder_id', proceed, errors)

        if proceed:
            location = Location(
                location_name=location_name,
                longitude=longitude,
                latitude = latitude,
                address = address,
                reminder_id = reminder_id
            )
            db.session.add(location)
            db.session.commit()
            last_location = db.session.query(Location).filter_by(location_name=location_name).one()
            reminder = db.session.query(Reminder).filter_by(id=reminder_id).first()
            reminder.location_id = last_location.id
            db.session.commit()
            return location, errors
        else:
            return None, errors

    def post(self, *args, **kwargs):
        json_data = request.get_json(force=True)
        location, errors = self._create_location(json_data))

        if location is not None:
            location = Location.query.filter_by(location_name=json_data['location_name']).first()
            result = location_schema.dump(location)
            return result, 201
        else:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400
