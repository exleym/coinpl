import quandl
from coinpl import create_app

app = create_app()
quandl.ApiConfig.api_key = app.config['QUANDL_KEY']

data = quandl.get("BCHARTS/BITSTAMPUSD")
print(data)

