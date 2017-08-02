import requests
from requests.exceptions import HTTPError
import json

class GDAX(object):

    BASE_URL = 'https://api.gdax.com'

    def __init__(self):
        pass

    def get_candles(self, product, start, end, granularity=60):
        request = '/{}/candles?start={}&end={}&granularity={}'.format(
            product, start, end, granularity
        )
        resp = requests.get(self.BASE_URL + request)
        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            raise HTTPError('The server failed to return products')

    def get_currencies(self):
        url = self.BASE_URL + '/currencies'
        resp = requests.get(url)
        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            raise HTTPError('The server failed to return currencies')

    def get_products(self):
        url = self.BASE_URL + '/products'
        resp = requests.get(url)
        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            raise HTTPError('The server failed to return products')


if __name__ == '__main__':
    gdax = GDAX()
    gdax.get_products()