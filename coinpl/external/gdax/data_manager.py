from sqlalchemy.orm import sessionmaker
from coinpl.models import Currency, Product
from coinpl.external.services import GDAX


class GDAXDataManager(object):
    def __init__(self, eng):
        self.eng = eng
        self.Session = sessionmaker(bind=eng)
        self.data_svc = GDAX()

    def populate_fixed_resources(self):
        self._populate_currencies()
        self._populate_products()

    def backfill_historical_data(product='ETH-USD', months=1, granularity=60):
        pass

    def _populate_currencies(self):
        currencies = self.data_svc.get_currencies()
        session = self.Session()
        for c in currencies:
            session.add(Currency(symbol=c['id'], name=c['name'],
                                 min_size=float(c['min_size'])))
        session.commit()
        session.close()

    def _populate_products(self):
        products = self.data_svc.get_products()
        session = self.Session()
        currencies = session.query(Currency).all()
        currencies = {c.symbol: c.id for c in currencies}

        for p in products:
            p['symbol'] = p['id']
            p['base_currency_id'] = currencies[p['base_currency']]
            p['quote_currency_id'] = currencies[p['quote_currency']]
            p = {k: v for k, v in p.items() if k not in ['id', 'base_currency',
                                                         'status', 'status_message',
                                                         'quote_currency']}
            session.add(Product(**p))
        session.commit()
        session.close()