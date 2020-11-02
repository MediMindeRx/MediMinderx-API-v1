import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from api import create_app, db
from api.database.models import User
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class PatchuserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.user_1 = User(name='zzz 1')
        self.user_1.insert()

        # adding extra padding in here to ensure we strip() it off later
        self.payload = {
            'id': f'{self.user_1.id}',
            'name': ' new_name '
        }

    # def tearDown(self):
    #     db.session.remove()
    #     db_drop_everything(db)
    #     self.app_context.pop()

    def test_happypath_patch_a_user(self):
        payload = deepcopy(self.payload)

        response = self.client.patch(
            f'/api/v1/users',
            json=payload,
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))

        assert_payload_field_type_value(
            self, data['data']['attributes'], 'name', str, payload['name'].strip()
        )
        user_id = data['data']['id']

    def test_sadpath_patch_blank_name(self):
        payload = deepcopy(self.payload)
        payload['name'] = ''

        response = self.client.patch(
            f'/api/v1/users',
            json=payload,
            content_type='application/json'
        )
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', int, 400)
        assert_payload_field_type_value(
            self, data, 'errors', list,
            ["required 'name' parameter is blank"]
        )
