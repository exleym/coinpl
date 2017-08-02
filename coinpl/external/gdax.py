import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from sqlalchemy.orm import sessionmaker
from coinpl.models import Currency, Product
from coinpl.external.data import GDAX


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
            p = {k: v for k, v in p.items() if k not in ['id', 'base_currency', 'quote_currency']}
            session.add(Product(**p))
        session.commit()
        session.close()


        # Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

if __name__ == '__main__':
    API_KEY = '315443e0f369c537777706d0188296fd'
    API_SECRET = 'skmXJVpCUHGe1s2E3/oK9GjZyySeeeIOO3yIyexjviNRl3oW4Zb8RPTjL4Lt4HXpr2BhFpxF61sxyAuw/eEj5w=='
    API_PASS = 'h84kwM2BkZqXG9OaZs2Y'
    api_url = 'https://api.gdax.com/'
    auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

    # Get accounts
    r = requests.get(api_url + 'accounts', auth=auth)
    print(r.json())


