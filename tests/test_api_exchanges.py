import json
import unittest
from coinpl import create_app
from tests import create_exchanges


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

    def test_create_exchange(self):
        with self.app.test_request_context():
            exchange = {
                'name': 'Test Exchange 01',
                'symbol': 'TEST',
                'url': 'http://foo.bar/1',
                'active': True
            }
            rv = self.create_resource('exchanges', exchange)
            data = json.loads(rv.data)
            self.assertEqual(data["name"], "Test Exchange 01")

    def test_get_exchange(self):
        with self.app.test_request_context():
            create_exchanges(self.client)
            resp = self.get_resource('exchange', resource_id=1)
            data = json.loads(resp.data)
            self.assertEqual(data["name"], 'Coinbase')

    def test_get_multiple_exchanges(self):
        with self.app.test_request_context():
            create_exchanges(self.client)
            resp = self.get_resource('exchanges')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[1]['name'], 'GDAX')

    def test_missing_exchange(self):
        with self.app.test_request_context():
            resp = self.get_resource('exchange', resource_id=1)
            self.assertEqual(resp.status_code, 404)
