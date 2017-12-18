from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import User
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, users can retrieve currency information by id,
# retrieve a list of users, add new users, update existing users.
@api_v1.route('/user', methods=['POST'])
def create_user():
    """ POST to /api/v1.0/users will create a new User object
    """
    if not request.json:
        return error_out(MissingJSONError())
    expected_fields = ['alias', 'password', 'first_name', 'last_name', 'email']
    data = request.json

    # Ensure that required fields have been included in JSON data
    if not verify_required_fields(data, expected_fields):
        return error_out(PostValidationError())
    session = get_session(current_app)
    user = User(alias=data['alias'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                moderator=False,
                admin=False)
    session.add(user)
    try:
        session.commit()
    except:
        return error_out(DatabaseIntegrityError())
    user = session.query(User).filter(User.alias == data["alias"]).first()
    return jsonify(user.shallow_json), 201


@api_v1.route('/user/<int:user_id>', methods=['GET'])
def read_user_by_id(user_id):
    session = get_session(current_app)
    exch = session.query(User).filter(User.id == user_id).first()
    if not exch:
        return error_out(MissingResourceError('User'))
    return jsonify(exch.shallow_json), 200


@api_v1.route('/user/', methods=['GET'])
def read_users():
    session = get_session(current_app)
    users = session.query(User).all()
    if not users:
        return error_out(MissingResourceError('User'))
    return jsonify([user.shallow_json for user in users]), 200


@api_v1.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """ PUT request to /api/user/<exchane_id> will update User object
        <id> with fields passed
    """
    session = get_session(current_app)
    put_data = request.json
    if not put_data:
        return error_out(MissingJSONError())
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return error_out(MissingResourceError('User'))
    for k, v in put_data.items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    return jsonify(user.shallow_json)


@api_v1.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ DELETE request to /api/v1.0/user/<user_id> will delete the
        target User object from the database
    """
    session = get_session(current_app)
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return error_out(MissingResourceError('User'))
    session.delete(user)
    session.commit()
    return jsonify(200)
