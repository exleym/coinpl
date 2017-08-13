from datetime import datetime
from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Cut
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing cut information
# With these API endpoints, users can retrieve cut information by id,
# retrieve a list of cuts, add new cuts, update existing cuts.
@api_v1.route('/cuts', methods=['POST'])
def create_cut():
    """ POST to /api/v1.0/cuts will create a new Cut object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['wallet_id', 'effective', 'cut_time', 'pl_version_id']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    cut = Cut(wallet_id=data['wallet_id'],
              effective=datetime.strptime(data['effective'], "%Y-%m-%d %H:%M:%S"),
              cut_time=datetime.strptime(data['effective'], "%Y-%m-%d %H:%M:%S"),
              pl_version_id=data['pl_version_id'])
    session.add(cut)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    return jsonify(cut.shallow_json), 201


@api_v1.route('/cut/<int:cut_id>', methods=['GET'])
def read_cut_by_id(cut_id):
    session = get_session(current_app)
    cut = session.query(Cut).filter(Cut.id == cut_id).first()
    if not cut:
        return error_out(MissingResourceError('Cut'))
    return jsonify(cut.shallow_json), 200


@api_v1.route('/cuts/', methods=['GET'])
def read_cuts():
    session = get_session(current_app)
    cuts = session.query(Cut).all()
    if not cuts:
        return error_out(MissingResourceError('Cut'))
    return jsonify([cut.shallow_json for cut in cuts]), 200


@api_v1.route('/cut/<int:cut_id>', methods=['PUT'])
def update_cut(cut_id):
    """ PUT request to /api/cut/<cut_id> will update Cut object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    cut = session.query(Cut).filter(Cut.id == cut_id).first()
    if not cut:
        return error_out(MissingResourceError('Cut'))
    for k, v in put_data.items():
        setattr(cut, k, v)
    session.add(cut)
    session.commit()
    return jsonify(cut.shallow_json)


@api_v1.route('/cut/<int:cut_id>', methods=['DELETE'])
def delete_cut(cut_id):
    """ DELETE request to /api/v1.0/cut/<cut_id> will delete the
        target Cut object from the database
    """
    session = get_session(current_app)
    cut = session.query(Cut).filter(Cut.id == cut_id).first()
    if not cut:
        return error_out(MissingResourceError('Cut'))
    session.delete(cut)
    session.commit()
    return jsonify(200)
