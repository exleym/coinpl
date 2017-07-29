from flask import Blueprint, current_app, render_template, send_file
from flask import jsonify, redirect, request, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user

from coinpl import get_session
from coinpl.models import Wallet

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1.0')


@api_v1.route('/wallets', methods=['GET'])
def wallets():
    session = get_session(current_app)
    wallets = session.query(Wallet).all()
    return jsonify([w.to_json() for w in wallets])
