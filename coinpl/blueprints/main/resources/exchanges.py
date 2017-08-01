from coinpl import get_session
from coinpl.blueprints.main import main
from coinpl.blueprints.main.forms import ExchangeForm
from coinpl.models import Exchange
from flask import abort, current_app, redirect, render_template, url_for
from flask_login import login_required


@main.route('/exchanges/<int:exchange_id>', methods=['GET'])
@login_required
def exchange(exchange_id):
    session = get_session(current_app)
    exchg = session.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not exchg:
        abort(404)
    return render_template('main/resources/exchange.html', exchange=exchg)


@main.route('/exchanges', methods=['GET'])
@login_required
def exchanges():
    session = get_session(current_app)
    exchg = session.query(Exchange).all()
    return render_template('main/resources/exchanges.html',
                           exchanges=exchg)


@main.route('/exchanges/add', methods=['GET', 'POST'])
@login_required
def add_exchange():
    exchange_form = ExchangeForm()
    session = get_session(current_app)
    if exchange_form.validate_on_submit():
        exch = Exchange(
            name=exchange_form.name.data,
            url=exchange_form.url.data
        )
        session.add(exch)
        session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/quick_form.html', header='Add an Exchange',
                           form=exchange_form)