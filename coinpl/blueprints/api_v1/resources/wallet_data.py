from datetime import datetime
from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import WalletData
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, we can retrieve WalletData information by
# id, retrieve a history of WalletData, add new data, update existing data.
@api_v1.route('/wallet_data', methods=['POST'])
def create_wallet_data():
    """ POST to /api/v1.0/wallet_data will create a new WalletData object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['wallet_id', 'cut_id', 'effective', 'nav',
                       'invested_value']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    wd = WalletData(wallet_id=data['wallet_id'],
                    cut_id=data['cut_id'],
                    effective=datetime.strptime(data['effective'], '%Y-%m-%d').date(),
                    nav=data['nav'],
                    invested_value=data['invested_value'])
    session.add(wd)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    return jsonify(wd.shallow_json), 201


@api_v1.route('/wallet_data/<int:wallet_data_id>', methods=['GET'])
def read_wallet_data_by_id(wallet_data_id):
    session = get_session(current_app)
    wd = session.query(WalletData).filter(WalletData.id == wallet_data_id).first()
    if not wd:
        return error_out(MissingResourceError('WalletData'))
    return jsonify(wd.shallow_json), 200


@api_v1.route('/wallet_data/', methods=['GET'])
def read_wallet_data():
    session = get_session(current_app)
    wallet_data = session.query(WalletData).all()
    if not wallet_data:
        return error_out(MissingResourceError('WalletData'))
    return jsonify([wd.shallow_json for wd in wallet_data]), 200


@api_v1.route('/wallet_data/<int:wallet_data_id>', methods=['PUT'])
def update_wallet_data(wallet_data_id):
    """ PUT request to /api/wallet/<wallet_id> will update
        WalletData object <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    wd = session.query(WalletData).filter(WalletData.id == wallet_data_id).first()
    if not wd:
        return error_out(MissingResourceError('WalletData'))
    for k, v in put_data.items():
        setattr(wd, k, v)
    session.add(wd)
    session.commit()
    return jsonify(wd.shallow_json), 200


@api_v1.route('/wallet_data/<wallet_data_id>', methods=['DELETE'])
def delete_wallet_data(wallet_data_id):
    """ DELETE request to /api/v1.0/wallet/<wallet_id> will delete the
        target WalletData object from the database
    """
    session = get_session(current_app)
    wd = session.query(WalletData).filter(WalletData.id == wallet_data_id).first()
    if not wd:
        return error_out(MissingResourceError('WalletData'))
    session.delete(wd)
    session.commit()
    return jsonify(200)
