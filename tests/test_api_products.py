import json
import unittest
from coinpl import create_app
from tests import create_currencies, create_products


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

    def test_create_product(self):
        with self.app.test_request_context():
            create_currencies(client=self.client)
            dta = {
                'symbol': 'ETH-USD',
                'base_currency_id': 1,
                'quote_currency_id': 2,
                'base_min_size': 0.01,
                'base_max_size': 1000000,
                'quote_increment': 0.01,
                'display_name': 'ETH/USD',
                'margin_enabled': False
            }
            rv = self.create_resource('products', dta)
            data = json.loads(rv.data)
            self.assertEqual(data['symbol'], 'ETH-USD')

    def test_get_product(self):
        with self.app.test_request_context():
            create_products(client=self.client)
            resp = self.get_resource('product', resource_id=1)
            data = json.loads(resp.data)
            self.assertEqual(data["symbol"], 'ETH-USD')

    def test_get_multiple_products(self):
        with self.app.test_request_context():
            create_products(client=self.client)
            resp = self.get_resource('products')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['symbol'], 'ETH-USD')

    def test_missing_product(self):
        with self.app.test_request_context():
            resp = self.get_resource('product', resource_id=1)
            self.assertEqual(resp.status_code, 404)
