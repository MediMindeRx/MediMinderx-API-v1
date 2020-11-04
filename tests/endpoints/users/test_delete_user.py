import json
import unittest
from unittest.mock import patch
from copy import deepcopy

from api import create_app, db
from api.database.models import User
from tests import db_drop_everything, assert_payload_field_type_value


class DeleteUserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.user_1 = User(name='zzz 1')
        self.user_1.insert()

        self.payload = { 'id': f'{self.user_1.id}' }

    # def tearDown(self):
    #     db.session.remove()
    #     db_drop_everything(db)
    #     self.app_context.pop()


    def test_happypath_delete_a_user(self):
        payload = deepcopy(self.payload)

        response = self.client.delete(
            '/api/v1/users', json=payload,
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('{\n    "message": "User has been successfully deleted"\n}\n', response.data.decode('utf-8'))

        # ensure it's really gone by getting a 404 if we try to fetch it again
        response = self.client.get(
            f'/api/v1/users/{self.user_1.id}'
        )
        self.assertEqual(404, response.status_code)

    # def test_sadpath_delete_bad_id_user(self):
    #     payload_1 = { 'id': '1'}
    #
    #     response = self.client.delete(
    #         '/api/v1/users', json=payload_1,
    #         content_type='application/json'
    #     )
    #     self.assertEqual(404, response.status_code)
        #
        # data = json.loads(response.data.decode('utf-8'))
        # assert_payload_field_type_value(self, data, 'error', int, 404)
        # assert_payload_field_type_value(self, data, 'success', bool, False)
        # assert_payload_field_type_value(
        #     self, data, 'message', str, 'resource not found'
        # )
