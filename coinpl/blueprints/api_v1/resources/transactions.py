from datetime import datetime
from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Transaction
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, transactions can retrieve currency information by
# id, retrieve a list of transactions, add new transactions, update existing
# transactions.
@api_v1.route('/transactions', methods=['POST'])
def create_transaction():
    """ POST to /api/v1.0/transactions will create a new Transaction object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['currency_id', 'exchange_id', 'wallet_id', 'trade_time',
                       'quantity', 'execution_price', 'commission']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    transaction = Transaction(currency_id=data['currency_id'],
                              exchange_id=data['exchange_id'],
                              wallet_id=data['wallet_id'],
                              trade_time=datetime.strptime(data['trade_time'], '%Y-%m-%d %H:%M:%S'),
                              quantity=data['quantity'],
                              execution_price=data['execution_price'],
                              commission=data['commission'])
    session.add(transaction)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    return jsonify(transaction.shallow_json), 201


@api_v1.route('/transaction/<int:transaction_id>', methods=['GET'])
def read_transaction_by_id(transaction_id):
    session = get_session(current_app)
    txn = session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        return error_out(MissingResourceError('Transaction'))
    return jsonify(txn.shallow_json), 200


@api_v1.route('/transactions/', methods=['GET'])
def read_transactions():
    session = get_session(current_app)
    txns = session.query(Transaction).all()
    if not txns:
        return error_out(MissingResourceError('Transaction'))
    return jsonify([transaction.shallow_json for transaction in txns]), 200


@api_v1.route('/transaction/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    """ PUT request to /api/transaction/<transaction_id> will update
        Transaction object <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return error_out(MissingResourceError('Transaction'))
    for k, v in put_data.items():
        setattr(transaction, k, v)
    session.add(transaction)
    session.commit()
    return jsonify(transaction.shallow_json), 200


@api_v1.route('/transaction/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """ DELETE request to /api/v1.0/transaction/<transaction_id> will delete the
        target Transaction object from the database
    """
    session = get_session(current_app)
    transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return error_out(MissingResourceError('Transaction'))
    session.delete(transaction)
    session.commit()
    return jsonify(200)
