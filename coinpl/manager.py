from coinpl import connect, get_session
from coinpl.models import Market, Product
from coinpl.external.services import GDAX


class DataManager(object):
    def __init__(self, app):
        self.app = app
        self.eng = connect(app)

    def update_market(self, product):
        session = get_session(self.app)
        prod = session.query(Product).filter(Product.symbol == product).first()
        if not prod:
            return None
        gdax = GDAX()
        resp = gdax.get_market(prod.symbol)
        mkt = Market(
            sequence=resp['sequence'],
            product_id=prod.id,
            bid_price=float(resp['bids'][0][0]),
            bid_size=float(resp['bids'][0][1]),
            bid_parties=int(resp['bids'][0][2]),
            ask_price=float(resp['asks'][0][0]),
            ask_size=float(resp['asks'][0][1]),
            ask_parties=int(resp['asks'][0][2])
        )
        session.add(mkt)
        session.commit()
        return mkt


class CutManager(object):

    def __init__(self, app):
        self.app = app
        self.eng = connect(self.app)

    def calculate(self, effective):
        """ Calculate holdings and PL and generate Cuts
        :param effective:
        :return:
        """