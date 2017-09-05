import datetime
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from coinpl.models import Currency, DailyPrice, DataSource, Exchange, Product
from coinpl.external.services import Quandl


class QuandlDataManager(object):

    def __init__(self, eng, app):
        self.eng = eng
        self.Session = sessionmaker(bind=eng)
        self.data_svc = Quandl(quandl_key=app.config['QUANDL_KEY'])

    def backfill_historical_data(self, currency='BTC', quote_currency='USD', months=12, exchange_id=None):
        session = self.Session()

        if not exchange_id:
            exchanges = session.query(Exchange).filter(Exchange.sources.any(DataSource.id)).all()
        else:
            exchanges = session.query(Exchange).filter(Exchange.id == exchange_id).all()
        qdl = session.query(DataSource).filter(DataSource.name == 'Quandl').one()
        prd = "{}-{}".format(currency, quote_currency)
        prod = session.query(Product).filter(Product.symbol == prd).one()
        for x in exchanges:
            data = self.data_svc.get_historical_data(
                'BCHARTS', '{}{}'.format(x.symbol, quote_currency)
            )

            data.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume ({})'.format(currency): 'volume',
                'Weighted Price': 'wtd_price'

            }, inplace=True)
            data = data.loc[:, ['open', 'high', 'low', 'close', 'volume', 'wtd_price']]
            data.loc[:, 'date'] = data.index
            data.loc[:, 'exchange_id'] = x.id
            data.loc[:, 'source_id'] = qdl.id
            data.loc[:, 'product_id'] = prod.id
            data.to_sql('daily_prices', self.eng, if_exists='append', index=False)

    def update_data(self, currency='BTC', quote_currency='USD', exchange_id=None):
        session = self.Session()

        if not exchange_id:
            exchanges = session.query(Exchange).filter(
                Exchange.sources.any(DataSource.id)).all()
        else:
            exchanges = session.query(Exchange).filter(
                Exchange.id == exchange_id).all()
        qdl = session.query(DataSource).filter(DataSource.name == 'Quandl').one()
        prd = "{}-{}".format(currency, quote_currency)
        prod = session.query(Product).filter(Product.symbol == prd).one()
        for x in exchanges:
            latest_value = self._get_latest_value(
                exchange_id=x.id,
                source_id=qdl.id,
                product_id=prod.id
            )

            data = self.data_svc.get_historical_data(
                'BCHARTS', '{}{}'.format(x.symbol, quote_currency),
                date_range=(latest_value.date, datetime.date.today())
            )

            data.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume ({})'.format(currency): 'volume',
                'Weighted Price': 'wtd_price'

            }, inplace=True)
            data = data.loc[:, ['open', 'high', 'low', 'close', 'volume', 'wtd_price']]
            data.loc[:, 'date'] = data.index
            data.loc[:, 'exchange_id'] = x.id
            data.loc[:, 'source_id'] = qdl.id
            data.loc[:, 'product_id'] = prod.id
            data.to_sql('daily_prices', self.eng, if_exists='append', index=False)

    def _get_latest_value(self, exchange_id, source_id, product_id):
        session = self.Session()
        last = session.query(DailyPrice).filter(
            DailyPrice.exchange_id == exchange_id,
            DailyPrice.source_id == source_id,
            DailyPrice.product_id == product_id
        ).order_by(desc(DailyPrice.date)).limit(1).all()
        return last