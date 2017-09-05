from datetime import datetime
from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Currency
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, users can retrieve currency information by id,
# retrieve a list of currencies, add new currencies, update existing currencies.
@api_v1.route('/currency', methods=['POST'])
def create_currency():
    """ POST to /api/v1.0/currencies will create a new Currency object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['symbol', 'name', 'min_size', 'ipo_date', 'currency_limit']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    currency = Currency(symbol=data['symbol'],
                        name=data['name'],
                        min_size=data['min_size'],
                        ipo_date=datetime.strptime(data['ipo_date'], "%Y-%m-%d"),
                        currency_limit=data['currency_limit'])
    session.add(currency)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    return jsonify(currency.shallow_json), 201


@api_v1.route('/currency/<int:currency_id>', methods=['GET'])
def read_currency_by_id(currency_id):
    shallow = False if request.args.get('shallow') == 'false' else True
    session = get_session(current_app)
    currency = session.query(Currency).filter(Currency.id == currency_id).first()
    if not currency:
        return error_out(MissingResourceError('Currency'))
    if shallow:
        return jsonify(currency.shallow_json), 200
    return jsonify(currency.json), 200


@api_v1.route('/currency/', methods=['GET'])
def read_currencies():
    session = get_session(current_app)
    currencies = session.query(Currency).all()
    if not currencies:
        return error_out(MissingResourceError('Currency'))
    return jsonify([currency.shallow_json for currency in currencies]), 200


@api_v1.route('/currency', methods=['PUT'])
def update_currency():
    """ PUT request to /api/currency/<currency_id> will update Currency object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    currency = session.query(Currency).filter(Currency.id == put_data['id']).first()
    if not currency:
        return error_out(MissingResourceError('Currency'))
    for k, v in put_data.items():
        setattr(currency, k, v)
    session.add(currency)
    session.commit()
    return jsonify(currency.shallow_json)


@api_v1.route('/currency/<int:currency_id>', methods=['DELETE'])
def delete_currency(currency_id):
    """ DELETE request to /api/v1.0/currency/<currency_id> will delete the
        target Currency object from the database
    """
    session = get_session(current_app)
    currency = session.query(Currency).filter(Currency.id == currency_id).first()
    if not currency:
        return error_out(MissingResourceError('Currency'))
    session.delete(currency)
    session.commit()
    return jsonify(200)
