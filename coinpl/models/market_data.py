from datetime import datetime
from sqlalchemy import (Column, BigInteger, Boolean, Date, DateTime, Float,
                        ForeignKey, Integer, String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import time
from werkzeug.security import check_password_hash, generate_password_hash

from coinpl.models import Base


class DailyPrice(Base):
    __tablename__ = 'daily_prices'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    source_id = Column(Integer, ForeignKey('data_sources.id'))
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
            self.close, self.source_id
        )

    @property
    def shallow_json(self):
        return {
            k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"
        }

    @property
    def highchart_json(self):
        return [time.mktime(self.date.timetuple()) * 1000, self.close]