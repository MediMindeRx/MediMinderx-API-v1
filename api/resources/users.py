import datetime
import json

import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import db
from api.database.models import User


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


def _user_payload(user):
    return {
        'id': user.id,
        'name': user.name
    }

class UsersResource(Resource):
    """
    this Resource file is for our /users endpoints which don't require
    a resource ID in the URI path
    """
    def _create_user(self, data):
        """
        methods that start with an underscore are understood, in Python
        circles, to be a "private" method that shouldn't be directly called
        elsewhere. There's no true "private" arrangement in Python.
        """
        proceed = True
        errors = []

        proceed, name, errors = _validate_field(
            data, 'name', proceed, errors)

        if proceed:
            user = User(
                name=name
            )
            db.session.add(user)
            db.session.commit()
            return user, errors
        else:
            return None, errors

    def post(self, *args, **kwargs):
        user, errors = self._create_user(json.loads(request.data))
        if user is not None:
            user_payload = _user_payload(user)
            user_payload['success'] = True
            # return user_payload, 201
            return 'added to db', 201
        else:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400

    def get(self, *args, **kwargs):
        users = User.query.order_by(
            User.name.asc()
        ).all()
        results = [_user_payload(user) for user in users]
        return {
            'success': True,
            'results': results
        }, 200


class UserResource(Resource):
    """
    this Resource file is for our /users endpoints which do require
    a resource ID in the URI path
    GET /users/6
    DELETE /users/3
    PATCH /users/18
    """
    def get(self, *args, **kwargs):
        user_id = int(bleach.clean(kwargs['user_id'].strip()))
        user = None
        try:
            user = db.session.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            return abort(404)

        user_payload = _user_payload(user)
        user_payload['success'] = True
        return user_payload, 200

    def patch(self, *args, **kwargs):
        user_id = int(bleach.clean(kwargs['user_id'].strip()))
        user = None
        try:
            user = db.session.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            return abort(404)

        proceed = True
        errors = []
        data = json.loads(request.data)
        proceed, name, errors = _validate_field(
            data, 'name', proceed, errors, missing_okay=True)

        if not proceed:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400

        if name and len(name.strip()) > 0:
            user.name = name
        user.update()

        user_payload = _user_payload(user)
        user_payload['success'] = True
        return user_payload, 200

    def delete(self, *args, **kwargs):
        user_id = kwargs['user_id']
        user = None
        try:
            user = db.session.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            return abort(404)

        user.delete()
        return {}, 204
