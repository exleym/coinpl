import json
import unittest
from sqlalchemy import create_engine
from coinpl import create_app, get_db
from coinpl.models import Base


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
            rv = self.create_resource('users', dta)
            data = json.loads(rv.data)
            self.assertEqual(data["alias"], "jerry")
            self.assertEqual(data["id"], 1)

    def test_get_user(self):
        with self.app.test_request_context():
            dta = {
                'alias': 'jerry',
                'password': 'cornell77',
                'first_name': 'Jerry',
                'last_name': 'Garcia',
                'email': 'jgarcia@gmail.com'
            }
            self.create_resource('users', dta)
            resp = self.get_resource('user', resource_id=1)
            data = json.loads(resp.data)
            self.assertEqual(data["alias"], 'jerry')

    def test_get_multiple_users(self):
        with self.app.test_request_context():
            users = ['Jerry', 'Bobby', 'Phil', 'Mickey', 'Bill']
            names = {'Jerry': 'Garcia', 'Bobby': 'Weir', 'Phil': 'Lesh',
                     'Mickey': 'Hart', 'Bill': 'Kreutzmann'}
            for u in users:
                dta = {
                    'alias': u.lower(),
                    'password': 'cornell77',
                    'first_name': u.title(),
                    'last_name': names[u],
                    'email': '{}{}@gmail.com'.format(u.lower(),
                                                     names[u].lower())
                }
                self.create_resource('users', dta)
            resp = self.get_resource('users')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 5)
            self.assertEqual(data[0]['alias'], 'jerry')

    def test_missing_user(self):
        with self.app.test_request_context():
            resp = self.get_resource('user', resource_id=1)
            self.assertEqual(resp.status_code, 404)
