from flask import Blueprint, current_app, render_template, send_file
from flask import redirect, request, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user

from coinpl import get_session

main = Blueprint('main', __name__, url_prefix='')


@main.route('/')
def index():
    session = get_session(current_app)
    return "<h1>Hello, World!</h1>"
