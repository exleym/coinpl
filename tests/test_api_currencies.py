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

    def test_create_currency(self):
        with self.app.test_request_context():
            rv = self.create_resource('currencies', {'symbol': 'TC1',
                                                     'name': 'Test Currency 01',
                                                     'min_size': 0.001,
                                                     'ipo_date': '2014-1-1',
                                                     'currency_limit': 9000})
            data = json.loads(rv.data)
            self.assertEqual(data["symbol"], "TC1")
            self.assertEqual(data["id"], 1)

    def test_get_currency(self):
        with self.app.test_request_context():
            rv = self.create_resource('currencies', {'symbol': 'TC1',
                                                     'name': 'Test Currency 01',
                                                     'min_size': 0.001,
                                                     'ipo_date': '2014-1-1',
                                                     'currency_limit': 9000})
            resp = self.get_resource('currency', resource_id=1)
            data = json.loads(resp.data)
            self.assertEqual(data["name"], 'Test Currency 01')

    def test_get_multiple_currencies(self):
        with self.app.test_request_context():
            for i in range(5):
                dta = {'symbol': 'TC{}'.format(i),
                       'name': 'Test Currency 0{}'.format(i),
                       'min_size': 0.001,
                       'ipo_date': '2014-1-1',
                       'currency_limit': 9000}
                self.create_resource('currencies', dta)
            resp = self.get_resource('currencies')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 5)
            self.assertEqual(data[1]['name'], 'Test Currency 01')

    def test_missing_currency(self):
        with self.app.test_request_context():
            resp = self.get_resource('currency', resource_id=1)
            self.assertEqual(resp.status_code, 404)
