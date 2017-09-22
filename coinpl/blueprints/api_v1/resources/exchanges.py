from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Exchange
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, users can retrieve currency information by id,
# retrieve a list of exchanges, add new exchanges, update existing exchanges.
@api_v1.route('/exchanges', methods=['POST'])
def create_exchange():
    """ POST to /api/v1.0/exchanges will create a new Exchange object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['name', 'symbol', 'url', 'active']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    exchange = Exchange(name=data["name"],
                        symbol=data["symbol"],
                        url=data["url"],
                        active=data["active"])
    session.add(exchange)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    exchange = session.query(Exchange).filter(Exchange.name == data["name"]).first()
    return jsonify(exchange.shallow_json), 201


@api_v1.route('/exchange/<int:exchange_id>', methods=['GET'])
def read_exchange_by_id(exchange_id):
    session = get_session(current_app)
    exch = session.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not exch:
        return error_out(MissingResourceError('Exchange'))
    return jsonify(exch.json), 200


@api_v1.route('/exchanges/', methods=['GET'])
def read_exchanges():
    session = get_session(current_app)
    exch = session.query(Exchange).all()
    if not exch:
        return error_out(MissingResourceError('Exchange'))
    return jsonify([x.shallow_json for x in exch]), 200


@api_v1.route('/exchange/<int:exchange_id>', methods=['PUT'])
def update_exchange(exchange_id):
    """ PUT request to /api/exchange/<exchange_id> will update Exchange object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    exchange = session.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not exchange:
        return error_out(MissingResourceError('Exchange'))
    for k, v in put_data.items():
        setattr(exchange, k, v)
    session.add(exchange)
    session.commit()
    return jsonify(exchange.shallow_json)


@api_v1.route('/exchange/<exchange_id>', methods=['DELETE'])
def delete_exchange(exchange_id):
    """ DELETE request to /api/v1.0/exchange/<exchange_id> will delete the
        target Exchange object from the database
    """
    session = get_session(current_app)
    exchange = session.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not exchange:
        return error_out(MissingResourceError('Exchange'))
    session.delete(exchange)
    session.commit()
    return jsonify(200)