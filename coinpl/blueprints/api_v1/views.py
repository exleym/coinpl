from flask import Blueprint, current_app, render_template, send_file
from flask import jsonify, redirect, request, url_for, flash
from coinpl.external.gdax import GDAXOrderManager

from flask_login import login_user, logout_user, login_required, current_user

from coinpl import get_session
from coinpl.models import Exchange, Market, Product, Wallet

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1.0')


@api_v1.route('/exchanges', methods=['POST'])
def create_exchange():
    session = get_session(current_app)
    import pdb; pdb.set_trace()
    package = request.get_json()
    try:
        assert "name" in package.keys()
    except AssertionError:
        raise KeyError("You must pass the appropriate keys to the endpoint")
    session.add(Exchange(name=package["name"], url=package["url"]))
    session.commit()
    session.close()
    return 200


@api_v1.route('/exchanges/', methods=['GET'])
def get_exchanges():
    session = get_session(current_app)
    exch = session.query(Exchange).all()
    resp = [x.to_json() for x in exch]
    return jsonify(resp)


@api_v1.route('/exchanges/<int:exchange_id>', methods=['GET'])
def get_exchange_by_id(exchange_id):
    session = get_session(current_app)
    exch = session.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not exch:
        return jsonify({'Error': 404}), 404
    return jsonify(exch.to_json()), 200


@api_v1.route('/wallets', methods=['GET'])
def wallets():
    session = get_session(current_app)
    wallets = session.query(Wallet).all()
    return jsonify([w.to_json() for w in wallets])


@api_v1.route('/markets/<currency>', methods=['GET'])
def markets(currency):
    crncy = currency + '-USD'
    session = get_session(current_app)
    markets = session.query(Market).filter(Product.symbol == crncy).limit(10)
    return jsonify([m.to_json() for m in markets])


@api_v1.route('/account_stats', methods=['GET'])
def account_stats():
    gdax = GDAXOrderManager(current_app)
    print(gdax.get_account_stats())
    return jsonify(gdax.get_account_stats())