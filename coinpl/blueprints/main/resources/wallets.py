from coinpl import get_session
from coinpl.blueprints.main import main
from coinpl.blueprints.main.forms import WalletForm
from coinpl.external import download_qr_code_from_google
from coinpl.models import Currency, Exchange, Transaction, Wallet
from flask import abort, current_app, redirect, render_template, url_for
from flask_login import current_user, login_required
import os


@main.route('/wallets/<int:wallet_id>')
@login_required
def wallet(wallet_id):
    session = get_session(current_app)
    wallet = session.query(Wallet).filter(Wallet.id == wallet_id).first()
    #holdings = session.query(Transaction, func.sum(Transaction.quantity)) \
    #                  .filter(Transaction.wallet.owner_id==current_user.id)
    holdings = 420
    if not wallet:
        abort(404)

    qr = '/coinpl/coinpl/static/img/qrcodes/wallet_qr_{}.png'.format(wallet.id)
    if not os.path.isfile(qr):
        download_qr_code_from_google(wallet=wallet)
    return render_template('main/resources/wallet.html', wallet=wallet,
                           holdings=holdings)


@main.route('/wallets', methods=['GET'])
@login_required
def wallets():
    session = get_session(current_app)
    crncy = session.query(Wallet).all()
    return render_template('main/resources/wallets.html',
                           wallets=crncy)


@main.route('/wallets/add', methods=['GET', 'POST'])
@login_required
def add_wallet():
    session = get_session(current_app)
    currencies = session.query(Currency).all()
    exchanges = session.query(Exchange).all()
    wallet_form = WalletForm()
    wallet_form.currency.choices = [(c.id, c.name) for c in currencies]
    wallet_form.exchange.choices = [(x.id, x.name) for x in exchanges]

    if wallet_form.validate_on_submit():
        wlt = Wallet(
            owner_id=current_user.id,
            currency_id=wallet_form.currency.data,
            exchange_id=wallet_form.exchange.data,
            name=wallet_form.name.data,
            inception_date=wallet_form.inception_date.data,
            address=wallet_form.address.data
        )
        session.add(wlt)
        session.commit()

        download_qr_code_from_google(wlt)
        return redirect(url_for('main.user_page',
                                user_name=current_user.alias))
    return render_template('main/quick_form.html', header='Add a Wallet',
                           form=wallet_form)
