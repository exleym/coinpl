import requests
from requests.exceptions import HTTPError
import json
import quandl

class Quandl(object):
    """ Quandl DataService for public API services.

    This class supports Market Data API requests for the Quandl BTC API.
    """

    def __init__(self, quandl_key):
        quandl.ApiConfig.api_key = quandl_key

    def get_historical_data(self, database_code, dataset_code):
        print('{}/{}'.format(database_code, dataset_code))
        data = quandl.get('{}/{}'.format(database_code, dataset_code))
        return data
