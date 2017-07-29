from datetime import datetime
from sqlalchemy import ( Column, Boolean, Date, DateTime, Float, ForeignKey,
                         Integer, String, Text )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    inception_date = Column(Date)

    def __repr__(self):
        return "<Wallet: {}>".format(self.name)


class WalletData(Base):
    """ Data from PL Cuts that represents the state of the Wallet
        These objects contain temporal data about a specific
        trading wallet at a specific point in time.

        For information about the PL System Cut that generated this
        object, see <WalletData>.cut
    """
    __tablename__ = 'wallet_data'
    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    cut_id = Column(Integer, ForeignKey('cuts.id'))
    effective = Column(Date)
    nav = Column(Float)
    invested_value = Column(Float)
    superceded = Column(Boolean, default=False)

    wallet = relationship('Wallet', backref='data')
    cut = relationship('Cut', backref='wallet_data', uselist=False)

    def __repr__(self):
        return "<WalletData: {}>".format(self.name)


class Coin(Base):
    __tablename__ = 'coins'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    ipo_date = Column(Date)
    coin_limit = Column(Integer)

    def __repr__(self):
        return "<Coin: {}>".format(self.name)


class Cut(Base):
    __tablename__ = 'cuts'
    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    effective = Column(DateTime)
    cut_time = Column(DateTime, default=datetime.now)
    pl_version_id = Column(Integer, ForeignKey('pl_versions.id'))


    wallet = relationship('Wallet', backref='cuts')
    pl_version = relationship('PLVersion', backref='cuts')

    def __repr__(self):
        return "<Cut: {:d} ({})>".format(self.id,
                                         self.cut_date.strftime('%Y-%m-%d'))


class Exchange(Base):
    __tablename__ = 'exchanges'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    url = Column(String(256))

    def __repr__(self):
        return "<Exchange: {}>".format(self.name)


class PLVersion(Base):
    __tablename__ = 'pl_versions'
    id = Column(Integer, primary_key=True)
    release_date = Column(DateTime, nullable=False)
    build_notes = Column(Text)
    pr_url = Column(String(256))

    def __repr__(self):
        return "<PLVersion: {:d} ({})>".format(self.id,
                                               self.release_date.strftime('%Y-%m-%d'))


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer, ForeignKey('coins.id'))
    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    trade_time = Column(DateTime, nullable=False)
    quantity = Column(Float, nullable=False)
    execution_price = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)

    coin = relationship('Coin', backref='trades')
    exchange = relationship('Exchange', backref='trades')

    def __repr__(self):
        return "<Trade: {} {}>".format(
            self.name,
            self.trade_time.strftime('%Y-%m-%d %H%M%S')
        )


class Holding(Base):
    __tablename__ = 'holdings'
    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    coin_id = Column(Integer, ForeignKey('coins.id'))
    cut_id = Column(Integer, ForeignKey('cuts.id'))
    cut_date = Column(Date)
    quantity = Column(Float)
    price = Column(Float)

    coin = relationship('Coin', backref='holdings')
    wallet = relationship('Wallet', backref='holdings')
    cut = relationship('Cut', backref='holdings')

    def __repr__(self):
        return "<Holding {:d}: {} {}>".format(self.id,
                                              self.coin.code,
                                              self.cut_date.strftime('%Y-%m-%d'))
