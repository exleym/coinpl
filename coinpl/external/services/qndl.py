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

    def get_historical_data(self, database_code, dataset_code, date_range=None):
        if not date_range:
            data = quandl.get('{}/{}'.format(database_code, dataset_code))
        else:
            data = quandl.get('{}/{}'.format(database_code, dataset_code),
                              start_date=date_range[0].strftime('%Y-%m-%d'),
                              end_date=date_range[1].strftime('%Y-%m-%d'))
        return data
