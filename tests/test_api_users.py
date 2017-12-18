import json
import unittest
from coinpl import create_app
from tests import create_users


class TestModels(unittest.TestCase):
    API_BASE = '/api/v1.0/'

    def create_resource(self, resource_name, data):
        url = self.API_BASE + resource_name
        r = self.client.post(url, data=json.dumps(data),
                             content_type='application/json')
        return r

    def get_resource(self, resource_name, resource_id=None):
        url = '/api/v1.0/{}/'.format(resource_name)
        if resource_id:
            url = '/api/v1.0/{}/{}'.format(resource_name, resource_id)
        return self.client.get(url, content_type='application/json')

    def setUp(self):
        self.app = create_app('test')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_create_user(self):
        with self.app.test_request_context():
            dta = {
                'alias': 'jerry',
                'password': 'cornell77',
                'first_name': 'Jerry',
                'last_name': 'Garcia',
                'email': 'jgarcia@gmail.com'
            }
            rv = self.create_resource('user', dta)
            data = json.loads(rv.data)
            self.assertEqual(data["alias"], "jerry")
            self.assertEqual(data["id"], 1)

    def test_get_user(self):
        with self.app.test_request_context():
            create_users(self.client)
            resp = self.get_resource('user', resource_id=1)
            data = json.loads(resp.data)
            self.assertEqual(data["alias"], 'jerry')

    def test_get_multiple_users(self):
        with self.app.test_request_context():
            create_users(self.client)
            resp = self.get_resource('user')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 5)
            self.assertEqual(data[0]['alias'], 'jerry')

    def test_missing_user(self):
        with self.app.test_request_context():
            resp = self.get_resource('user', resource_id=1)
            self.assertEqual(resp.status_code, 404)
