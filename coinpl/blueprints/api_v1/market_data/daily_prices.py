from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask import current_app, jsonify, request
from coinpl import get_session
from coinpl.models import DailyPrice
from coinpl.util.errors import (DatabaseIntegrityError,
                                MissingResourceError,
                                MissingJSONError,
                                PostValidationError)

from coinpl.blueprints.api_v1 import api_v1, error_out, verify_required_fields


# API Routes for accessing and managing currency information
# With these API endpoints, users can retrieve currency information by id,
# retrieve a list of currencies, add new currencies, update existing currencies.
@api_v1.route('/datasets/daily-prices/product/<int:product_id>/exchange/<int:exchange_id>/source/<int:source_id>', methods=['GET'])
def read_daily_prices(product_id, exchange_id, source_id):
    end_date = date.today()
    if request.args.get('endDate'):
        end_date = datetime.strptime(request.args.get('startDate'), '%Y-%m-%d').date()

    start_date =  end_date - relativedelta(days=365)
    if request.args.get('startDate'):
        start_date = datetime.strptime(request.args.get('startDate'), '%Y-%m-%d').date()

    session = get_session(current_app)

    dly_prices = session.query(DailyPrice) \
                        .filter(DailyPrice.product_id == product_id) \
                        .filter(DailyPrice.exchange_id == exchange_id) \
                        .filter(DailyPrice.source_id == source_id) \
                        .filter(DailyPrice.date >= start_date) \
                        .filter(DailyPrice.date <= end_date) \
                        .order_by(DailyPrice.date) \
                        .all()
    if not dly_prices:
        return error_out(MissingResourceError('DailyPrice'))
    return jsonify([px.shallow_json for px in dly_prices]), 200

