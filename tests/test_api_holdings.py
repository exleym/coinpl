import json
import unittest
from coinpl import create_app
from tests import (create_currencies, create_holdings, create_wallets,
                   create_cuts)


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

    def test_create_holding(self):
        with self.app.test_request_context():
            create_currencies(self.client)
            create_wallets(self.client)
            create_cuts(self.client)
            holding = {
                'wallet_id': 1,
                'currency_id': 1,
                'cut_id': 1,
                'cut_date': '2017-8-1',
                'quantity': 42,
                'price': 300.00
            }
            rv = self.create_resource('holdings', holding)
            data = json.loads(rv.data)
            self.assertEqual(data["id"], 1)

    def test_get_holding(self):
        with self.app.test_request_context():
            create_holdings(self.client)
            resp = self.get_resource('holding', resource_id=1)
            data = json.loads(resp.data)
            self.assertEqual(data["wallet_id"], 1)

    def test_get_multiple_holdings(self):
        with self.app.test_request_context():
            create_holdings(self.client)
            resp = self.get_resource('holdings')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 4)
            self.assertEqual(data[0]['wallet_id'], 1)

    def test_missing_holding(self):
        with self.app.test_request_context():
            resp = self.get_resource('holding', resource_id=1)
            self.assertEqual(resp.status_code, 404)
