from datetime import datetime
from sqlalchemy import (Column, BigInteger, Boolean, Date, DateTime, Float,
                        ForeignKey, Integer, String, Table, Text)
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from coinpl.models import Base


exchange_sources = Table('exchange_sources', Base.metadata,
    Column('exchange_id', Integer, ForeignKey('exchanges.id')),
    Column('source_id', Integer, ForeignKey('data_sources.id'))
)


exchange_products = Table('exchange_products', Base.metadata,
    Column('exchange_id', Integer, ForeignKey('exchanges.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)


class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    alert_type_id = Column(Integer, ForeignKey('alert_types.id'))
    approved = Column(Boolean, default=False)
    approving_user_id = Column(Integer, ForeignKey('users.id'))
    approval_timestamp = Column(DateTime)

    type = relationship('AlertType')

    @property
    def shallow_json(self):
        data = {
            "id": self.id,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "alert_type_id": self.alert_type_id,
            "approved": self.approved,
            "approving_user_id": self.approving_user_id,
            "approval_timestamp": self.approval_timestamp
        }
        return data

    @property
    def json(self):
        data = self.shallow_json
        data.update({
            "type": self.type.shallow_json
        })
        return data

    def __repr__(self):
        return "<Alert: {} (type={})>".format(self.id,
                                              self.alert_type.name)


class AlertType(Base):
    __tablename__ = 'alert_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    short_name = Column(String(16))

    @property
    def shallow_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "short_name": self.short_name
        }


class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(3), unique=True, nullable=False)
    name = Column(String(128), unique=True, nullable=False)
    min_size = Column(Float)
    ipo_date = Column(Date)
    currency_limit = Column(Integer)

    products = relationship('Product', backref='base_currency',
                            foreign_keys='Product.base_currency_id')
    can_buy = relationship('Product', backref='quote_currency',
                           foreign_keys='Product.quote_currency_id')

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

    @property
    def json(self):
        data = self.shallow_json
        data.update({
            "products": [p.shallow_json for p in self.products],
            "can_buy": [p.shallow_json for p in self.can_buy]
        })
        return data

    def __repr__(self):
        return "<Currency: {}>".format(self.symbol)


class CurrencyState(Base):
    __tablename__ = 'currency_states'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    def __repr__(self):
        return "<CurrencyState: {}>".format(self.name)


class CurrencyStateHistory(Base):
    __tablename__ = 'currency_state_history'
    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    currency_state_id = Column(Integer, ForeignKey('currency_states.id'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

    currency = relationship('Currency', backref='state_history')
    state = relationship('CurrencyState')

    def __repr__(self):
        return "<CurrencyStateHistory: {} = {} ({} - {})>".format(
            self.currency.symbol,
            self.state.name,
            self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        )


class Cut(Base):
    __tablename__ = 'cuts'
    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    effective = Column(DateTime)
    cut_time = Column(DateTime, default=datetime.now)
    pl_version_id = Column(Integer, ForeignKey('pl_versions.id'))

    wallet = relationship('Wallet', backref='cuts')
    pl_version = relationship('PLVersion', backref='cuts')

    @property
    def shallow_json(self):
        return {
            "id": self.id,
            "wallet_id": self.wallet_id,
            "effective": self.effective.strftime('%Y-%m-%d %H:%M:%S'),
            "cut_time": self.cut_time.strftime('%Y-%m-%d %H:%M:%S'),
            "pl_version_id": self.pl_version_id
        }

    def __repr__(self):
        return "<Cut: {:d} ({})>".format(self.id,
                                         self.cut_time.strftime('%Y-%m-%d'))


class DataSource(Base):
    __tablename__ = 'data_sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    url = Column(String(256))

    exchanges = relationship('Exchange', secondary=exchange_sources, backref='sources')

    def __repr__(self):
        return "<DataSource: {}>".format(self.name)

    @property
    def shallow_json(self):
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }


class Exchange(Base):
    __tablename__ = 'exchanges'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(8), unique=True)
    name = Column(String(128), unique=True)
    url = Column(String(256))
    active = Column(Boolean)

    @property
    def shallow_json(self):
        return {"id": self.id,
                "name": self.name,
                "symbol": self.symbol,
                "url": self.url,
                "active": self.active}

    @property
    def json(self):
        data = self.shallow_json
        data.update({
            "sources": [s.shallow_json for s in self.sources]
        })
        return data

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

    @property
    def shallow_json(self):
        return {
            "id": self.id,
            "wallet_id": self.wallet_id,
            "currency_id": self.currency_id,
            "cut_id": self.cut_id,
            "cut_date": self.cut_date.strftime('%Y-%m-%d'),
            "quantity": self.quantity,
            "price": self.price
        }

    def __repr__(self):
        return "<Holding {}: {} {}>".format(self.id,
                                            self.currency.code,
                                            self.cut_date.strftime(
                                                '%Y-%m-%d'
                                            ))


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


class PLVersion(Base):
    __tablename__ = 'pl_versions'
    id = Column(Integer, primary_key=True)
    release_date = Column(DateTime, nullable=False)
    build_notes = Column(Text)
    pr_url = Column(String(256))

    def __repr__(self):
        return "<PLVersion: {:d} ({})>".format(self.id,
                                               self.release_date.strftime(
                                                   '%Y-%m-%d'
                                               ))


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

    exchanges = relationship('Exchange', secondary=exchange_products, backref='products')

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
            self.trade_time.strftime('%Y-%m-%d %H:%M:%S')
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
    #base_currency_id = Column(Integer, ForeignKey('currencies.id'))

    #base_currency = relationship('Currency', backref='base_users')

    @property
    def shallow_json(self):
        return {
            "id": self.id,
            "alias": self.alias,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "moderator": self.moderator,
            "admin": self.admin,
            "created": self.created.strftime('%Y-%m-%d %H:%M:%S'),
            "updated": self.updated.strftime('%Y-%m-%d %H:%M:%S')
        }

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        print("checking password hash ...")
        if check_password_hash(self.password_hash, password):
            print("password checks out!")
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
    address = Column(String(34))
    deactivated = Column(Boolean)

    owner = relationship('User', backref='wallets',
                         primaryjoin="and_(User.id==Wallet.owner_id, "
                         "Wallet.deactivated==False)")
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
                "inception_date": self.inception_date.strftime('%Y-%m-%d'),
                "deactivated": self.deactivated
                }

    @property
    def full_json(self):
        data = self.shallow_json
        data.update({"currency": self.currency.shallow_json})
        data.update({"exchange": self.exchange.shallow_json})
        data.update({"owner": self.owner.shallow_json})
        return data


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

    @property
    def shallow_json(self):
        return {
            "id": self.id,
            "wallet_id": self.wallet_id,
            "cut_id": self.cut_id,
            "effective": self.effective.strftime('%Y-%m-%d'),
            "nav": self.nav,
            "invested_value": self.invested_value,
            "superceded": self.superceded
        }

    def __repr__(self):
        return "<WalletData: {}>".format(self.name)
