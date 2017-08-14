import json
import unittest
from coinpl import create_app
from tests import create_products, create_markets


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

    def test_create_market(self):
        with self.app.test_request_context():
            create_products(self.client)
            dta = {
                'timestamp': '2017-8-13 12:54:00',
                'sequence': 99999,
                'product_id': 1,
                'bid_price': 294.5,
                'bid_size': 200,
                'bid_parties': 4,
                'ask_price': 296.13,
                'ask_size': 344.24,
                'ask_parties': 8
            }
            rv = self.create_resource('markets', dta)
            data = json.loads(rv.data)
            self.assertEqual(data["sequence"], 99999)

    def test_get_market(self):
        with self.app.test_request_context():
            create_markets(self.client)
            resp = self.get_resource('market', resource_id=1)
            data = json.loads(resp.data)
            self.assertEqual(data['sequence'], 12345)

    def test_get_multiple_markets(self):
        with self.app.test_request_context():
            create_markets(self.client)
            resp = self.get_resource('markets')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 3)
            self.assertEqual(data[0]['sequence'], 12345)

    def test_missing_market(self):
        with self.app.test_request_context():
            resp = self.get_resource('market', resource_id=1)
            self.assertEqual(resp.status_code, 404)
