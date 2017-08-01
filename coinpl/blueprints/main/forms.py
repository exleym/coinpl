from flask_wtf import FlaskForm
from wtforms import (DateField, DateTimeField, FloatField, IntegerField,
                     SelectField, StringField, SubmitField)
from wtforms.validators import DataRequired


class CoinForm(FlaskForm):
    name = StringField('Currency Name')
    ipo_date = DateField('IPO Date')
    coin_limit = IntegerField('Coin Limit')
    submit = SubmitField('Add Trade')


class ExchangeForm(FlaskForm):
    name = StringField('Exchange Name', validators=[DataRequired()])
    url = StringField('Exchange URL', validators=[DataRequired()])
    submit = SubmitField('Add Exchange')


class WalletForm(FlaskForm):
    name = StringField('Wallet Name', validators=[DataRequired()])
    currency = SelectField('Currency', choices=[], coerce=int)
    exchange = SelectField('Exchange', choices=[], coerce=int)
    inception_date = DateField('Inception Date', validators=[DataRequired()])
    submit = SubmitField('Add Wallet')


class TradeForm(FlaskForm):
    trade_time = DateTimeField('Transaction Time')
    quantity = FloatField('Quantity')
    execution_price = FloatField('Execution Price')
    commission = FloatField('Commission Paid')
    submit = SubmitField('Add Trade')