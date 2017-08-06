import requests
from coinpl.external.gdax import CoinbaseExchangeAuth


# Create custom authentication for Exchange
class GDAXOrderManager(object):
    def __init__(self, app):
        self.api_key = app.config['COINBASE_API_KEY']
        self.api_secret = app.config['COINBASE_API_SECRET']
        self.api_pass = app.config['COINBASE_API_PASS']
        self.api_url = 'https://api.gdax.com/'
        self.auth = CoinbaseExchangeAuth(self.api_key, self.api_secret, self.api_pass)

    def get_account_stats(self):
        r = requests.get(self.api_url + 'accounts', auth=self.auth)
        return r.json()


