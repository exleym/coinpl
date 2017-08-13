"""
    Convenience functions for generating resources via API
"""
import json


URL_BASE = '/api/v1.0/'


def create_currencies(client):
    crncy = [
        {'symbol': 'ETH', 'name': 'Ethereum', 'min_size': 0.01,
         'currency_limit': 9000, 'ipo_date': '2014-1-1'},
        {'symbol': 'USD', 'name': 'US Dollar', 'min_size': 0.01,
         'currency_limit': None, 'ipo_date': '2014-1-1'},
        {'symbol': 'XBT', 'name': 'Bitcoin', 'min_size': 0.01,
         'currency_limit': 90000, 'ipo_date': '2014-1-1'}
    ]
    for c in crncy:
        client.post(URL_BASE + 'currencies',
                    data=json.dumps(c),
                    content_type='application/json')
    return 0


def create_exchanges(client):
    exchanges = [
        {'name': 'Coinbase', 'url': 'http://boo.yah'},
        {'name': 'GDAX', 'url': 'http://api.gdax.com'}
    ]
    for x in exchanges:
        client.post(URL_BASE + 'exchanges',
                    data=json.dumps(x),
                    content_type='application/json')
    return 0


def create_products(client):
    create_currencies(client)
    prd = [
        {'symbol': 'ETH-USD', 'base_currency_id': 1, 'quote_currency_id': 2,
         'base_min_size': 0.01, 'base_max_size': 1000, 'quote_increment': 0.01,
         'display_name': 'ETH/USD', 'margin_enabled': False},
        {'symbol': 'XBT-USD', 'base_currency_id': 3, 'quote_currency_id': 2,
         'base_min_size': 0.01, 'base_max_size': 1000, 'quote_increment': 0.01,
         'display_name': 'XBT/USD', 'margin_enabled': False}
    ]
    for p in prd:
        client.post(URL_BASE + 'products',
                    data=json.dumps(p),
                    content_type='application/json')
    return 0


def create_users(client):
    users = [
        {'alias': 'jerry', 'password': 'Athea82', 'first_name': 'Jerry',
         'last_name': 'Garcia', 'email': 'jgarcia@gmail.com'},
        {'alias': 'bobby', 'password': 'EstimatedPro', 'first_name': 'Bob',
         'last_name': 'Weir', 'email': 'bweir@gmail.com'},
        {'alias': 'phil', 'password': 'BassJumper', 'first_name': 'Phil',
         'last_name': 'Lesh', 'email': 'plesh@gmail.com'},
        {'alias': 'mickey', 'password': 'mouse', 'first_name': 'Mickey',
         'last_name': 'Hart', 'email': 'mhart@gmail.com'},
        {'alias': 'bill', 'password': 'badum-tsss', 'first_name': 'Bill',
         'last_name': 'Kreutzmann', 'email': 'bkreutzmann@gmail.com'},
    ]
    for u in users:
        client.post(URL_BASE + 'users',
                    data=json.dumps(u),
                    content_type='application/json')
    return 0