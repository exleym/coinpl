from datetime import datetime
from sqlalchemy import ( Column, BigInteger, Boolean, Date, DateTime, Float,
                         ForeignKey, Integer, String, Text )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

Base = declarative_base()


class Market(Base):
    __tablename__ = 'markets'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    sequence = Column(BigInteger, unique=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    bid_price = Column(Float)
    bid_size = Column(Float)
    bid_parties = Column(Integer)
    ask_price = Column(Float)
    ask_size = Column(Float)
    ask_parties = Column(Integer)

    product = relationship('Product', backref='market_data', uselist=False)

    def __repr__(self):
        return "<Market: {} {} {:.2f}x{:.2f}>".format(
            self.product.symbol,
            self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            self.bid_price,
            self.ask_price
        )

    @property
    def shallow_json(self):
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }


class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(3), unique=True, nullable=False)
    name = Column(String(128), unique=True, nullable=False)
    min_size = Column(Float)
    ipo_date = Column(Date)
    currency_limit = Column(Integer)

    @property
    def shallow_json(self):
        data = {
            "id": self.id,
            "symbol": self.symbol,
            "name": self.name,
            "min_size": self.min_size,
            "ipo_date": self.ipo_date,
            "currency_limit": self.currency_limit
        }
        return data

    def __repr__(self):
        return "<Currency: {}>".format(self.symbol)


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

    @property
    def shallow_json(self):
        return {"id": self.id, "name": self.name, "url": self.url}

    def __repr__(self):
        return "<Exchange: {}>".format(self.name)


class Holding(Base):
    __tablename__ = 'holdings'
    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    cut_id = Column(Integer, ForeignKey('cuts.id'))
    cut_date = Column(Date)
    quantity = Column(Float)
    price = Column(Float)

    currency = relationship('Currency', backref='holdings')
    wallet = relationship('Wallet', backref='holdings')
    cut = relationship('Cut', backref='holdings')

    def __repr__(self):
        return "<Holding {:d}: {} {}>".format(self.id,
                                              self.currency.code,
                                              self.cut_date.strftime('%Y-%m-%d'))


class PLVersion(Base):
    __tablename__ = 'pl_versions'
    id = Column(Integer, primary_key=True)
    release_date = Column(DateTime, nullable=False)
    build_notes = Column(Text)
    pr_url = Column(String(256))

    def __repr__(self):
        return "<PLVersion: {:d} ({})>".format(self.id,
                                               self.release_date.strftime('%Y-%m-%d'))


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(7), unique=True, nullable=False)
    base_currency_id = Column(Integer, ForeignKey('currencies.id'))
    quote_currency_id = Column(Integer, ForeignKey('currencies.id'))
    base_min_size = Column(Float)
    base_max_size = Column(Float)
    quote_increment = Column(Float)
    display_name = Column(String(7))
    margin_enabled = Column(Boolean)

    @property
    def shallow_json(self):
        return {k: v for k, v in self.__dict__.items()
                if k not in "_sa_instance_state"}

    def __repr__(self):
        return "<Product: {}>".format(self.display_name)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    trade_time = Column(DateTime, nullable=False)
    quantity = Column(Float, nullable=False)
    execution_price = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)

    currency = relationship('Currency', backref='trades')
    exchange = relationship('Exchange', backref='trades')
    wallet = relationship('Wallet', backref='trades')

    @property
    def shallow_json(self):
        return {
            'currency_id': self.currency_id,
            'exchange_id': self.exchange_id,
            'wallet_id': self.wallet_id,
            'trade_time': self.trade_time.strftime('%Y-%m-%d %H:%M:%S'),
            'quantity': self.quantity,
            'execution_price': self.execution_price,
            'commission': self.commission
        }

    def __repr__(self):
        return "<Trade: {} {}>".format(
            self.currency.name,
            self.trade_time.strftime('%Y-%m-%d %H%M%S')
        )


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    alias = Column(String(64), nullable=False, unique=True)
    password_hash = Column(String(128))
    first_name = Column(String(32))
    last_name = Column(String(32))
    email = Column(String(64), unique=True)
    moderator = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def shallow_json(self):
        return {k: v for k, v in self.__dict__.items()
                if k not in "_sa_instance_state"}

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        print("checking password hash ...")
        if check_password_hash(self.password_hash, password):
            print ("password checks out!")
        else:
            print("wrong password!")
        return check_password_hash(self.password_hash, password)

    def equals(self, other_user):
        if self.id == other_user.id:
            return True
        return False

    def __repr__(self):
        return "<User: %r>" % self.alias


class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    exchange_id = Column(Integer, ForeignKey('exchanges.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    name = Column(String(128), unique=True)
    inception_date = Column(Date)

    owner = relationship('User', backref='wallets')
    currency = relationship('Currency', backref='wallets')
    exchange = relationship('Exchange', backref='wallets')

    def __repr__(self):
        return "<Wallet: {}>".format(self.name)

    @property
    def shallow_json(self):
        return {"id": self.id,
                "owner_id": self.owner_id,
                "exchange_id": self.exchange_id,
                "currency_id": self.currency_id,
                "name": self.name,
                "inception_date": self.inception_date.strftime('%Y-%m-%d')
                }


class WalletData(Base):
    """ Data from PL Cuts that represents the state of the Wallet
        These objects contain temporal services about a specific
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

    wallet = relationship('Wallet', backref='services')
    cut = relationship('Cut', backref='wallet_data', uselist=False)

    def __repr__(self):
        return "<WalletData: {}>".format(self.name)