import json
import unittest
from sqlalchemy import create_engine
from coinpl import create_app, get_db
from coinpl.models import Base


class TestModels(unittest.TestCase):
    API_BASE = 'http://localhost:5000/api/v1.0/'

    def create_resource(self, resource_name, data):
        url = '/api/v1.0/' + resource_name
        r = self.client.post(url, data=json.dumps(data),
                             content_type='application/json')
        return r

    def get_resource(self, resource_name, resource_id):
        url = '/api/v1.0/{}/{}'.format(resource_name, resource_id)
        return self.client.get(url, content_type='application/json')

    def get_resources(self, resource_name):
        url = '/api/v1.0/{}/'.format(resource_name)
        return self.client.get(url, content_type='application/json')

    def setUp(self):
        self.app = create_app('test')
        self.con = get_db(self.app)
        Base.metadata.create_all(bind=self.con)
        self.client = self.app.test_client()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.con)

    def test_create_exchange(self):
        with self.app.test_request_context():
            rv = self.create_resource('exchanges', {'name': 'Test Exchange 01',
                                                   "url": "http://fooX.bar"})
            #import pdb; pdb.set_trace()
            data = json.loads(rv.data)
            self.assertEqual(data["name"], "Test Exchange 01")

    def test_get_exchange(self):
        with self.app.test_request_context():
            self.create_resource('exchanges', {'name': 'Test Exchange 01',
                                              "url": "http://fooY.bar"})
            resp = self.get_resource('exchanges', 1)
            data = json.loads(resp.data)
            self.assertEqual(data["name"], 'Test Exchange 01')

    def test_get_multiple_exchanges(self):
        with self.app.test_request_context():
            self.create_resource('exchanges', {'name': 'Exchange 01', "url": "http://foo1.bar"})
            self.create_resource('exchanges', {'name': 'Exchange 02', "url": "http://foo2.bar"})
            self.create_resource('exchanges', {'name': 'Exchange 03', "url": "http://foo3.bar"})
            resp = self.get_resources('exchanges')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 3)
            self.assertEqual(data[1]['name'], 'Exchange 02')

    def test_missing_exchange(self):
        pass
