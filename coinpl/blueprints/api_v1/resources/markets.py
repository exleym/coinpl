from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Market
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, users can retrieve currency information by id,
# retrieve a list of currencies, add new currencies, update existing currencies.
@api_v1.route('/market', methods=['POST'])
def create_market():
    """ POST to /api/v1.0/currencies will create a new market object
    """
    pass


@api_v1.route('/market/<int:market_id>', methods=['GET'])
def read_market_by_id(market_id):
    session = get_session(current_app)
    market = session.query(Market).filter(Market.id == market_id).first()
    if not market:
        return error_out(MissingResourceError('Market'))
    return jsonify(market.to_json())


@api_v1.route('/markets/<int:product_id>', methods=['GET'])
def read_markets(product_id):
    session = get_session(current_app)
    markets = session.query(Market).filter(Market.product_id==product_id).all()
    if not markets:
        return error_out(MissingResourceError('Market'))
    return jsonify([market.to_json() for market in markets])


@api_v1.route('/market/<int:market_id>', methods=['PUT'])
def update_market(market_id):
    """ PUT request to /api/currency/<market_id> will update market object
        <id> with fields passed
    """
    pass


@api_v1.route('/market/<int:market_id>', methods=['DELETE'])
def delete_market(market_id):
    """ DELETE request to /api/v1.0/market/<market_id> will delete the
        target market object from the database
    """
    pass