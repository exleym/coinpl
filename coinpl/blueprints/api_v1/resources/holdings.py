from datetime import datetime
from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Holding
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing holding information
# With these API endpoints, users can retrieve holding information by id,
# retrieve a list of holdings, add new holdings, update existing holdings.
@api_v1.route('/holdings', methods=['POST'])
def create_holding():
    """ POST to /api/v1.0/holdings will create a new Holding object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['wallet_id', 'currency_id', 'cut_id', 'cut_date',
                       'quantity', 'price']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    holding = Holding(wallet_id=data["wallet_id"],
                      currency_id=data["currency_id"],
                      cut_id=data["cut_id"],
                      cut_date=datetime.strptime(data["cut_date"], "%Y-%m-%d").date(),
                      quantity=data["quantity"],
                      price=data["price"])
    session.add(holding)
    try:
        session.commit()
    except:
       return error_out(DatabaseIntegrityError())
    return jsonify(holding.shallow_json), 201


@api_v1.route('/holding/<int:holding_id>', methods=['GET'])
def read_holding_by_id(holding_id):
    session = get_session(current_app)
    holding = session.query(Holding).filter(Holding.id == holding_id).first()
    if not holding:
        return error_out(MissingResourceError('Holding'))
    return jsonify(holding.shallow_json), 200


@api_v1.route('/holdings/', methods=['GET'])
def read_holdings():
    session = get_session(current_app)
    holdings = session.query(Holding).all()
    if not holdings:
        return error_out(MissingResourceError('Holding'))
    return jsonify([holding.shallow_json for holding in holdings]), 200


@api_v1.route('/holding/<int:holding_id>', methods=['PUT'])
def update_holding(holding_id):
    """ PUT request to /api/holding/<holding_id> will update Holding object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    holding = session.query(Holding).filter(Holding.id == holding_id).first()
    if not holding:
        return error_out(MissingResourceError('Holding'))
    for k, v in put_data.items():
        setattr(holding, k, v)
    session.add(holding)
    session.commit()
    return jsonify(holding.shallow_json)


@api_v1.route('/holding/<int:holding_id>', methods=['DELETE'])
def delete_holding(holding_id):
    """ DELETE request to /api/v1.0/holding/<holding_id> will delete the
        target Holding object from the database
    """
    session = get_session(current_app)
    holding = session.query(Holding).filter(Holding.id == holding_id).first()
    if not holding:
        return error_out(MissingResourceError('Holding'))
    session.delete(holding)
    session.commit()
    return jsonify(200)
