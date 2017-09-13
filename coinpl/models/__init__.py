from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from coinpl.models.models import (
    Alert,
    AlertType,
    Currency,
    Cut,
    DataSource,
    Exchange,
    Holding,
    Market,
    PLVersion,
    Product,
    Transaction,
    User,
    Wallet,
    WalletData
)

from coinpl.models.market_data import (
    DailyPrice
)