from datetime import datetime
from sqlalchemy import (Column, BigInteger, Boolean, Date, DateTime, Float,
                        ForeignKey, Integer, String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from coinpl.models import Base


class DataSource(Base):
    __tablename__ = 'data_sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    url = Column(String(256))

    def __repr__(self):
        return "<DataSource: {}>".format(self.name)

    @property
    def shallow_json(self):
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }


class DailyPrice(Base):
    __tablename__ = 'daily_prices'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    data_source_id = Column(Integer, ForeignKey('data_sources.id'))
    date = Column(Date, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    wtd_price = Column(Float)

    def __repr__(self):
        return "<DailyPrice {product: {}, date: {}, close: {}, source: {}}>".format(
            self.product_id, self.date.strftime('%Y-%m-%d'),
            self.close, self.data_source_id
        )

    @property
    def shallow_json(self):
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }
