from datetime import date
from flask import Flask, g, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from coinpl.models import Wallet
from settings import config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/', methods=['GET'])
def index():
    return "<h1>Hello, World!</h1>"


@app.route('/counter', methods=['GET'])
def counter():
    session = get_session(current_app)
    wallet = session.query(Wallet).all()
    if not wallet:
        wallet = Wallet(name='Test Wallet', inception_date=date(2017, 1, 1))
        session.add(wallet)
        session.commit()
    return "<h1>Wallet: {}!</h1>".format(wallet[0].name)


def get_db(app):
    if not hasattr(g, 'dbcon'):
        g.dbcon = connect(app)
    return g.dbcon


def get_session(app):
    Session = sessionmaker(bind=get_db(app))
    return Session()


def connect(app):
    eng = create_engine(config.DB_URI)
    return eng
