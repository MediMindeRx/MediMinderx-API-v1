import json
import unittest
from unittest.mock import patch

from api import create_app, db
from api.database.models import User
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class GetUserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.user_1 = User(name='zzz 1')
        self.user_1.insert()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db_drop_everything(db)
    #     self.app_context.pop()

    def test_happypath_get_a_user(self):
        response = self.client.get(
            f'/api/v1/users/{self.user_1.id}'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))

        assert_payload_field_type_value(
            self, data['data']['attributes'], 'name', str, self.user_1.name
        )
        user_id = data['data']['id']

    def test_endpoint_sadpath_bad_id_user(self):
        response = self.client.get(
            f'/api/v1/users/9999'
        )
        self.assertEqual(404, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 404)
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(
            self, data, 'message', str, 'resource not found'
        )
