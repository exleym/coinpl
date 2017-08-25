import json
from sqlalchemy.orm import sessionmaker
from coinpl.models import DataSource, Exchange


class LocalDataManager(object):

    def __init__(self, eng, app):
        self.eng = eng
        self.Session = sessionmaker(bind=eng)

    def fill_base_data(self):
        self.populate_exchanges()
        self.populate_data_sources()
        self.associate_exchanges_with_sources()

    def associate_exchanges_with_sources(self):
        session = self.Session()
        qndl = session.query(DataSource).filter(DataSource.name == 'Quandl').one()
        with open('./data/exchanges.json') as f_exchanges:
            exchanges = json.load(f_exchanges)
        for exch in exchanges:
            exchange = session.query(Exchange) \
                              .filter(Exchange.name==exch["name"]) \
                              .first()
            if exch["quandl_data"]:
                exchange.sources.append(qndl)
                session.add(exchange)
        session.commit()

    def populate_exchanges(self):
        session = self.Session()
        with open('./data/exchanges.json') as f_exchanges:
            exchanges = json.load(f_exchanges)
        for exch in exchanges:
            exchange = Exchange(
                name=exch["name"],
                symbol=exch["symbol"],
                url=exch["url"],
                active=exch["active"]
            )
            session.add(exchange)
        session.commit()
        session.close()
        return 0

    def populate_data_sources(self):
        session = self.Session()
        with open('./data/data_sources.json') as f_sources:
            sources = json.load(f_sources)
        for s in sources:
            source = DataSource(
                name=s["name"],
                url=s["url"]
            )
            session.add(source)
        session.commit()
        session.close()
        return 0