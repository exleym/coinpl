import json
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from coinpl import create_app, get_session
from coinpl.models import Base, Currency, Product
from coinpl.external.gdax import GDAXDataManager, GDAXOrderManager


class TestGdaxAPI(unittest.TestCase):
    con = create_engine('sqlite://')
    Session = sessionmaker(bind=con)

    def setUp(self):
        Base.metadata.create_all(bind=self.con)
        self.app = create_app('test')
        self.client = self.app.test_client()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.con)

    def test_gdax_resources(self):
        with self.app.test_request_context():
            dm = GDAXDataManager(self.con)
            dm.populate_fixed_resources()
            session = self.Session()
            currencies = session.query(Currency).all()
            self.assertTrue(len(currencies) > 0)

