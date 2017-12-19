from datetime import datetime
from flask import current_app, jsonify, request
import os
from coinpl import get_session
from coinpl.models import Wallet
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, wallets can retrieve currency information by
# id, retrieve a list of wallets, add new wallets, update existing
# wallets.
@api_v1.route('/wallet', methods=['POST'])
def create_wallet():
    """ POST to /api/v1.0/wallets will create a new Wallet object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['owner_id', 'exchange_id', 'currency_id', 'name',
                       'inception_date']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    wallet = Wallet(owner_id=data['owner_id'],
                    exchange_id=data['exchange_id'],
                    currency_id=data['currency_id'],
                    name=data['name'],
                    inception_date=datetime.strptime(data['inception_date'], '%Y-%m-%d').date())
    session.add(wallet)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    return jsonify(wallet.shallow_json), 201


@api_v1.route('/wallet/<int:wallet_id>', methods=['GET'])
def read_wallet_by_id(wallet_id):
    session = get_session(current_app)
    wallet = session.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        return error_out(MissingResourceError('Wallet'))
    return jsonify(wallet.shallow_json), 200


@api_v1.route('/wallet/', methods=['GET'])
def read_wallets():
    session = get_session(current_app)
    wallets = session.query(Wallet).all()
    if not wallets:
        return error_out(MissingResourceError('Wallet'))
    return jsonify([wallet.shallow_json for wallet in wallets]), 200


@api_v1.route('/wallet/<int:wallet_id>', methods=['PUT'])
def update_wallet(wallet_id):
    """ PUT request to /api/wallet/<wallet_id> will update
        Wallet object <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    wallet = session.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        return error_out(MissingResourceError('Wallet'))
    for k, v in put_data.items():
        setattr(wallet, k, v)
    session.add(wallet)
    session.commit()
    return jsonify(wallet.shallow_json), 200


@api_v1.route('/wallet/<wallet_id>', methods=['DELETE'])
def delete_wallet(wallet_id):
    """ DELETE request to /api/v1.0/wallet/<wallet_id> will delete the
        target Wallet object from the database
    """
    session = get_session(current_app)
    wallet = session.query(Wallet).filter(Wallet.id == wallet_id).first()
    qr_base = '/coinpl/coinpl/static/img/qrcodes/wallet_qr_{}.png'
    filename_qr = qr_base.format(wallet.id)
    if not wallet:
        return error_out(MissingResourceError('Wallet'))
    wallet.deactivated = True
    session.add(wallet)
    session.commit()

    if os.path.exists(filename_qr):
        os.remove(filename_qr)

    return jsonify(200)
