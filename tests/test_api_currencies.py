import json
import unittest
from coinpl import create_app
from tests import create_currencies


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

    def test_create_currency(self):
        with self.app.test_request_context():
            currency = {
                'symbol': 'TC1',
                'name': 'Test Currency 01',
                'min_size': 0.001,
                'ipo_date': '2014-1-1',
                'currency_limit': 9000
            }
            rv = self.create_resource('currencies', currency)
            data = json.loads(rv.data)
            self.assertEqual(data["symbol"], "TC1")
            self.assertEqual(data["id"], 1)

    def test_get_currency(self):
        with self.app.test_request_context():
            create_currencies(self.client)
            resp = self.get_resource('currency', resource_id=1)
            data = json.loads(resp.data)
            self.assertEqual(data["name"], 'Ethereum')

    def test_get_multiple_currencies(self):
        with self.app.test_request_context():
            create_currencies(self.client)
            resp = self.get_resource('currencies')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 3)
            self.assertEqual(data[0]['name'], 'Ethereum')

    def test_missing_currency(self):
        with self.app.test_request_context():
            resp = self.get_resource('currency', resource_id=1)
            self.assertEqual(resp.status_code, 404)
