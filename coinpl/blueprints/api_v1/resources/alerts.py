from datetime import datetime
from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import Alert
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing alert information
# With these API endpoints, users can retrieve alert information by id,
# retrieve a list of alerts, add new alerts, update existing alerts.
@api_v1.route('/alert', methods=['POST'])
def create_alert():
    """ POST to /api/v1.0/alerts will create a new Alert object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['alert_type', '']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not ('alert_type' in data.keys() or 'alert_type_id' in data.keys()):
        return error_out(PostValidationError())
    session = get_session(current_app)
    alert = Alert(timestamp=datetime.now(),
                  alert_type_id=data['alert_type_id'],
                  approved=False,
                  approving_user_id=None,
                  approval_timestamp=None)
    session.add(alert)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    return jsonify(alert.shallow_json), 201


@api_v1.route('/alert/<int:alert_id>', methods=['GET'])
def read_alert_by_id(alert_id):
    shallow = True if request.args.get('shallow') == 'true' else False
    session = get_session(current_app)
    alert = session.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return error_out(MissingResourceError('Alert'))
    if shallow:
        return jsonify(alert.shallow_json), 200
    return jsonify(alert.json), 200


@api_v1.route('/alert/', methods=['GET'])
def read_alerts():
    session = get_session(current_app)
    alerts = session.query(Alert).all()
    if not alerts:
        return error_out(MissingResourceError('Alert'))
    return jsonify([alert.shallow_json for alert in alerts]), 200


@api_v1.route('/alert', methods=['PUT'])
def update_alert():
    """ PUT request to /api/alert/<alert_id> will update Alert object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    alert = session.query(Alert).filter(Alert.id == put_data['id']).first()
    if not alert:
        return error_out(MissingResourceError('Alert'))
    for k, v in put_data.items():
        setattr(alert, k, v)
    session.add(alert)
    session.commit()
    return jsonify(alert.shallow_json)


@api_v1.route('/alert/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """ DELETE request to /api/v1.0/alert/<alert_id> will delete the
        target Alert object from the database
    """
    session = get_session(current_app)
    alert = session.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return error_out(MissingResourceError('Alert'))
    session.delete(alert)
    session.commit()
    return jsonify(200)
