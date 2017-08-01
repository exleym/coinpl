from flask import abort, Blueprint, current_app, render_template
from flask import redirect, url_for
from flask_login import login_required

from coinpl import get_session
from coinpl.blueprints.main.forms import CoinForm, ExchangeForm, TradeForm, WalletForm
from coinpl.models import Transaction, User, Wallet

main = Blueprint('main', __name__, url_prefix='')

@main.route('/')
def index():
    session = get_session(current_app)
    return render_template('index.html')


@main.route('/user/<user_name>', methods=['GET'])
@login_required
def user_page(user_name):
    session = get_session(current_app)
    user = session.query(User).filter(User.alias == user_name).first()
    if not user:
        abort(404)
    return render_template('main/user.html', user=user)


@main.route('/wallet/<wallet_id>/trades/add', methods=['GET', 'POST'])
@login_required
def manual_trade(wallet_id):
    trade_form = TradeForm()
    session = get_session(current_app)
    wallet = session.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        abort(404)
    if trade_form.validate_on_submit():
        trade = Transaction(
            coin_id=wallet.coin_id,
            exchange_id=wallet.exchange_id,
            wallet_id=wallet.id,
            trade_time=trade_form.trade_time.data,
            quantity=trade_form.quantity.data,
            execution_price=trade_form.execution_price.data,
            commission=trade_form.commission.data
        )
        session.add(trade)
        session.commit()
        return redirect(url_for('main.wallet', wallet_id=wallet_id))
    return render_template('main/quick_form.html', header='Add a Trade',
                           form=trade_form)


from coinpl.blueprints.main.resources.currencies import (
    add_currency,
    currency,
    currencies
)
from coinpl.blueprints.main.resources.exchanges import (
    add_exchange,
    exchange,
    exchanges
)
from coinpl.blueprints.main.resources.wallets import (
    add_wallet,
    wallet,
    wallets
)