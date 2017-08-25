from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Market
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, markets can retrieve currency information by id,
# retrieve a list of markets, add new markets, update existing markets.
@api_v1.route('/markets', methods=['POST'])
def create_market():
    """ POST to /api/v1.0/markets will create a new Market object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['sequence', 'product_id', 'bid_price', 'bid_size',
                       'bid_parties', 'ask_price', 'ask_size', 'ask_parties',
                       'timestamp']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    market = Market(sequence=data['sequence'],
                    product_id=data['product_id'],
                    bid_price=data['bid_price'],
                    bid_size=data['bid_size'],
                    bid_parties=data['bid_parties'],
                    ask_price=data['ask_price'],
                    ask_size=data['ask_size'],
                    ask_parties=data['ask_parties'])
    session.add(market)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    market = session.query(Market).filter(Market.sequence == data["sequence"]).first()
    return jsonify(market.shallow_json), 201


@api_v1.route('/market/<int:market_id>', methods=['GET'])
def read_market_by_id(market_id):
    session = get_session(current_app)
    exch = session.query(Market).filter(Market.id == market_id).first()
    if not exch:
        return error_out(MissingResourceError('Market'))
    return jsonify(exch.shallow_json), 200


@api_v1.route('/markets/', methods=['GET'])
def read_markets():
    session = get_session(current_app)
    markets = session.query(Market).all()
    if not markets:
        return error_out(MissingResourceError('Market'))
    return jsonify([market.shallow_json for market in markets]), 200


@api_v1.route('/product/<int:product_id>/markets/')
def read_markets_for_product(product_id):
    session = get_session(current_app)
    markets = session.query(Market).filter(Market.product_id==product_id).all()
    if not markets:
        return error_out(MissingResourceError('Market'))
    return jsonify([market.shallow_json for market in markets]), 200


@api_v1.route('/market/<int:market_id>', methods=['PUT'])
def update_market(market_id):
    """ PUT request to /api/market/<exchane_id> will update Market object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    market = session.query(Market).filter(Market.id == market_id).first()
    if not market:
        return error_out(MissingResourceError('Market'))
    for k, v in put_data.items():
        setattr(market, k, v)
    session.add(market)
    session.commit()
    return jsonify(market.shallow_json), 200


@api_v1.route('/market/<market_id>', methods=['DELETE'])
def delete_market(market_id):
    """ DELETE request to /api/v1.0/market/<market_id> will delete the
        target Market object from the database
    """
    session = get_session(current_app)
    market = session.query(Market).filter(Market.id == market_id).first()
    if not market:
        return error_out(MissingResourceError('Market'))
    session.delete(market)
    session.commit()
    return jsonify(200)
