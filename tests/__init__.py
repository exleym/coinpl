"""
    Convenience functions for generating resources via API
"""
import json


URL_BASE = '/api/v1.0/'


def create_currencies(client):
    currencies = client.get(URL_BASE + 'currencies/')
    if currencies.status_code == 200:
        return 0
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


def create_cuts(client):
    cuts = client.get(URL_BASE + 'cuts/')
    if cuts.status_code == 200:
        return 0
    create_wallets(client)
    tstamp = "2017-8-1 17:00:00"
    tstamp2 = "2017-8-1 17:15:54"
    cuts = [
        {"wallet_id": 1, "effective": tstamp, "cut_time": tstamp2,
         "pl_version_id": 1},
        {"wallet_id": 2, "effective": tstamp, "cut_time": tstamp2,
         "pl_version_id": 1},
        {"wallet_id": 3, "effective": tstamp, "cut_time": tstamp2,
         "pl_version_id": 1},
        {"wallet_id": 4, "effective": tstamp, "cut_time": tstamp2,
         "pl_version_id": 1}
    ]
    for c in cuts:
        client.post(URL_BASE + 'cuts',
                    data=json.dumps(c),
                    content_type='application/json')
    return 0


def create_exchanges(client):
    exchanges = client.get(URL_BASE + 'exchanges/')
    if exchanges.status_code == 200:
        return 0
    exchanges = [
        {'name': 'Coinbase', 'url': 'http://boo.yah'},
        {'name': 'GDAX', 'url': 'http://api.gdax.com'}
    ]
    for x in exchanges:
        client.post(URL_BASE + 'exchanges',
                    data=json.dumps(x),
                    content_type='application/json')
    return 0


def create_holdings(client):
    cuts = client.get(URL_BASE + 'holdings/')
    if cuts.status_code == 200:
        return 0
    create_currencies(client)
    create_wallets(client)
    create_cuts(client)
    holdings = [
        {"wallet_id": 1, "currency_id": 1, "cut_id": 1, "cut_date": "2017-8-1",
         "quantity": 110, "price": 300},
        {"wallet_id": 2, "currency_id": 1, "cut_id": 2, "cut_date": "2017-8-1",
         "quantity": 120, "price": 300},
        {"wallet_id": 3, "currency_id": 1, "cut_id": 3, "cut_date": "2017-8-1",
         "quantity": 130, "price": 300},
        {"wallet_id": 4, "currency_id": 1, "cut_id": 4, "cut_date": "2017-8-1",
         "quantity": 140, "price": 300},
    ]
    for h in holdings:
        client.post(URL_BASE + 'holdings',
                    data=json.dumps(h),
                    content_type='application/json')
    return 0


def create_markets(client):
    markets = client.get(URL_BASE + 'markets/')
    if markets.status_code == 200:
        return 0
    mkt = [
        {'timestamp': '2017-8-13 12:54:00', 'sequence': 12345,
         'product_id': 1, 'bid_price': 294.5, 'bid_size': 200,
         'bid_parties': 4, 'ask_price': 296.13, 'ask_size': 344.24,
         'ask_parties': 8},
        {'timestamp': '2017-8-13 12:55:00', 'sequence': 12346,
         'product_id': 1, 'bid_price': 294.55, 'bid_size': 203.4,
         'bid_parties': 4, 'ask_price': 296.93, 'ask_size': 124.24,
         'ask_parties': 2},
        {'timestamp': '2017-8-13 12:56:00', 'sequence': 12347,
         'product_id': 1, 'bid_price': 294.5, 'bid_size': 452.46,
         'bid_parties': 11, 'ask_price': 295.67, 'ask_size': 110.83,
         'ask_parties': 5},
    ]
    for m in mkt:
        client.post(URL_BASE + 'markets',
                    data=json.dumps(m),
                    content_type='application/json')
    return 0


def create_products(client):
    products = client.get(URL_BASE + 'products/')
    if products.status_code == 200:
        return 0
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


def create_transactions(client):
    transactions = client.get(URL_BASE + 'transactions/')
    if transactions.status_code == 200:
        return 0
    create_currencies(client)
    create_exchanges(client)
    create_wallets(client)
    transactions = [
        {'currency_id': 1, 'exchange_id': 1, 'wallet_id': 1,
         'trade_time': '2017-8-11 13:54:00', 'quantity': 10,
         'execution_price': 255.00, 'commission': 0.25},
        {'currency_id': 1, 'exchange_id': 1, 'wallet_id': 1,
         'trade_time': '2017-8-13 12:54:00', 'quantity': -10,
         'execution_price': 294.00, 'commission': 0.25},
        {'currency_id': 3, 'exchange_id': 1, 'wallet_id': 2,
         'trade_time': '2017-8-11 17:54:00', 'quantity': 1,
         'execution_price': 2950.00, 'commission': 0.25},
        {'currency_id': 3, 'exchange_id': 1, 'wallet_id': 2,
         'trade_time': '2017-8-13 18:54:00', 'quantity': -1,
         'execution_price': 3232.00, 'commission': 0.25}
    ]
    for t in transactions:
        client.post(URL_BASE + 'transactions',
                    data=json.dumps(t),
                    content_type='application/json')
    return 0


def create_users(client):
    users = client.get(URL_BASE + 'users/')
    if users.status_code == 200:
        return 0
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


def create_wallets(client):
    wallets = client.get(URL_BASE + 'wallets/')
    if wallets.status_code == 200:
        return 0
    create_users(client)
    create_exchanges(client)
    create_currencies(client)
    wallets = [
        {'owner_id': 1, 'exchange_id': 1, 'currency_id': 1,
         'name': 'Test Wallet 01', 'inception_date': '2016-12-31'},
        {'owner_id': 2, 'exchange_id': 1, 'currency_id': 1,
         'name': 'Test Wallet 02', 'inception_date': '2016-12-31'},
        {'owner_id': 3, 'exchange_id': 1, 'currency_id': 1,
         'name': 'Test Wallet 03', 'inception_date': '2016-12-31'},
        {'owner_id': 4, 'exchange_id': 1, 'currency_id': 1,
         'name': 'Test Wallet 04', 'inception_date': '2016-12-31'},
    ]
    for w in wallets:
        client.post(URL_BASE + 'wallets',
                    data=json.dumps(w),
                    content_type='application/json')
    return 0


def create_wallet_data(client):
    wallet_data = client.get(URL_BASE + 'wallet_data/')
    if wallet_data.status_code == 200:
        return 0
    create_wallets(client)
    create_cuts(client)
    wallet_data = [
        {'wallet_id': 1, 'cut_id': 1, 'effective': '2017-8-10', 'nav': 9000,
         'invested_value': 5457.54},
        {'wallet_id': 2, 'cut_id': 2, 'effective': '2017-8-10', 'nav': 8000,
         'invested_value': 4457.54},
        {'wallet_id': 3, 'cut_id': 3, 'effective': '2017-8-10', 'nav': 7000,
         'invested_value': 3457.54},
        {'wallet_id': 4, 'cut_id': 4, 'effective': '2017-8-10', 'nav': 6000,
         'invested_value': 2457.54}
    ]
    for wd in wallet_data:
        client.post(URL_BASE + 'wallet_data',
                    data=json.dumps(wd),
                    content_type='application/json')
    return 0
