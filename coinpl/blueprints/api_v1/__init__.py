from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1.0')

def verify(json, required_fields, allowed_fields=None):
    if not allowed_fields:
        allowed_fields = []
    allowed_fields += required_fields
    passes_required = verify_required_fields(json, required_fields)
    passes_allowed = verify_allowed_fields(json, allowed_fields)
    return passes_required * passes_allowed


def verify_required_fields(json, expected_fields):
    for field in expected_fields:
        try:
            assert field in json
        except AssertionError:
            return False
    return True


def verify_allowed_fields(json, allowed_fields):
    """ Ensure that no fields are passed that are not permitted for a
        given resource.
        :param json: dictionary of POST data passed in request
        :param allowed_fields: list of strings of acceptable parameters
        :return: True if all parameters are allowed; else False
    """
    for k in json.keys():
        if k not in allowed_fields:
            return False
    return True


def error_out(error):
    return error.json_response(True)

from . resources.alerts import (create_alert,
                                read_alert_by_id,
                                read_alerts,
                                update_alert,
                                delete_alert)

from . resources.alert_types import (create_alert_type,
                                     read_alert_type_by_id,
                                     read_alert_types,
                                     update_alert_type,
                                     delete_alert_type)

from . resources.currencies import (create_currency,
                                    read_currency_by_id,
                                    read_currencies,
                                    update_currency,
                                    delete_currency)

from . resources.cuts import (create_cut,
                              read_cut_by_id,
                              read_cuts,
                              delete_cut)

from . resources.exchanges import (create_exchange,
                                   read_exchange_by_id,
                                   read_exchanges,
                                   update_exchange,
                                   delete_exchange)

from . resources.holdings import (create_holding,
                                  read_holding_by_id,
                                  read_holdings,
                                  update_holding,
                                  delete_holding)

from . resources.markets import (create_market,
                                 read_market_by_id,
                                 read_markets,
                                 update_market,
                                 delete_market)

from . resources.products import (create_product,
                                 read_product_by_id,
                                 read_products,
                                 update_product,
                                 delete_product)

from . resources.transactions import (create_transaction,
                                      read_transaction_by_id,
                                      read_transactions,
                                      update_transaction,
                                      delete_transaction)

from . resources.users import (create_user,
                               read_user_by_id,
                               read_users,
                               update_user,
                               delete_user)

from . resources.wallets import (create_wallet,
                                 read_wallet_by_id,
                                 read_wallets,
                                 update_wallet,
                                 delete_wallet)

from . resources.wallet_data import (create_wallet_data,
                                     read_wallet_data_by_id,
                                     read_wallet_data,
                                     update_wallet_data,
                                     delete_wallet_data)

from . market_data.daily_prices import (read_daily_prices,
                                        read_hs_prices)