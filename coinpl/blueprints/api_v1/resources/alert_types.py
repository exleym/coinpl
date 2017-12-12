from datetime import datetime
from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import AlertType
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing alert-type information
# With these API endpoints, users can retrieve alert-type information by id,
# retrieve a list of alert types, add new alert types, and
# update existing alert types.
@api_v1.route('/alert_type', methods=['POST'])
def create_alert_type():
    """ POST to /api/v1.0/alertTypes will create a new AlertType object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['name', 'short_name']
    data = request.json

    # Ensure that required fields have been included in JSON data
    verify_required_fields(data, expected_fields)
    session = get_session(current_app)
    alert_type = AlertType(name=data['name'],
                           short_name=data['short_name'])
    session.add(alert_type)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    return jsonify(alert_type.shallow_json), 201


@api_v1.route('/alert_type/<int:alert_type_id>', methods=['GET'])
def read_alert_type_by_id(alert_type_id):
    shallow = False if request.args.get('shallow') == 'false' else True
    session = get_session(current_app)
    alert_type = session.query(AlertType).filter(AlertType.id == alert_type_id).first()
    if not alert_type:
        return error_out(MissingResourceError('AlertType'))
    if shallow:
        return jsonify(alert_type.shallow_json), 200
    return jsonify(alert_type.json), 200


@api_v1.route('/alert_type/', methods=['GET'])
def read_alert_types():
    session = get_session(current_app)
    alert_types = session.query(AlertType).all()
    if not alert_types:
        return error_out(MissingResourceError('AlertType'))
    return jsonify([alert_type.shallow_json for alert_type in alert_types]), 200


@api_v1.route('/alert_type', methods=['PUT'])
def update_alert_type():
    """ PUT request to /api/alert_type/<alert_type_id> will update Alert object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    alert_type = session.query(AlertType).filter(AlertType.id == put_data['id']).first()
    if not alert_type:
        return error_out(MissingResourceError('AlertType'))
    for k, v in put_data.items():
        setattr(alert_type, k, v)
    session.add(alert_type)
    session.commit()
    return jsonify(alert_type.json)


@api_v1.route('/alert_type/<int:alert_type_id>', methods=['DELETE'])
def delete_alert_type(alert_type_id):
    """ DELETE request to /api/v1.0/alert/<alert_id> will delete the
        target Alert object from the database
    """
    session = get_session(current_app)
    alert_type = session.query(AlertType).filter(AlertType.id == alert_type_id).first()
    if not alert_type:
        return error_out(MissingResourceError('AlertType'))
    session.delete(alert_type)
    session.commit()
    return jsonify(200)
