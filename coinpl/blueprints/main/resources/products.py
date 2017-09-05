from coinpl import get_session
from coinpl.blueprints.main import main
from coinpl.blueprints.main.forms import CoinForm
from coinpl.models import Currency, Product
from coinpl.manager import DataManager
from flask import abort, current_app, redirect, render_template, url_for
from flask_login import login_required


@main.route('/products/<int:product_id>')
@login_required
def product(product_id):
    session = get_session(current_app)
    prd = session.query(Product).filter(Product.id == product_id).first()
    base = session.query(Currency).filter(Currency.id == prd.base_currency_id).first()
    quote = session.query(Currency).filter(Currency.id == prd.quote_currency_id).first()
    if not base or not quote:
        abort(404)
    return render_template('main/resources/product.html', product=prd,
                           base=base, quote=quote)
