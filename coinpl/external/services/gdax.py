import requests
from requests.exceptions import HTTPError
import json

class GDAX(object):
    """ GDAX DataService for public API services.

    This class supports API requests for the public GDAX API.
    It does not support private services requests or order generation.
    """

    BASE_URL = 'https://api.gdax.com'

    def __init__(self):
        pass

    def get_market(self, product):
        request = '/products/{}/book'.format(product)
        resp = requests.get(self.BASE_URL + request, params={'level': 1})
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