from coinpl import get_session
from coinpl.blueprints.main import main
from coinpl.blueprints.main.forms import CoinForm
from coinpl.models import Coin
from flask import abort, current_app, redirect, render_template, url_for
from flask_login import login_required


@main.route('/currencies/<int:currency_id>')
@login_required
def currency(currency_id):
    session = get_session(current_app)
    crncy = session.query(Coin).filter(Coin.id == currency_id).first()
    if not crncy:
        abort(404)
    return render_template('main/resources/currency.html', currency=crncy)


@main.route('/currencies', methods=['GET'])
@login_required
def currencies():
    session = get_session(current_app)
    crncy = session.query(Coin).all()
    return render_template('main/resources/currencies.html',
                           currencies=crncy)


@main.route('/currencies/add', methods=['GET', 'POST'])
@login_required
def add_currency():
    coin_form = CoinForm()
    session = get_session(current_app)
    if coin_form.validate_on_submit():
        coin = Coin(
            name=coin_form.name.data,
            ipo_date=coin_form.ipo_date.data,
            coin_limit=coin_form.coin_limit.data
        )
        session.add(coin)
        session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/quick_form.html', header='Add a Currency',
                           form=coin_form)
