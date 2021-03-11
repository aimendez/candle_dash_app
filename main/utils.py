import pandas as pd 
#import yfinance  as yf
import alpaca_trade_api as tradeapi 
from yahooquery import Ticker


api_ = tradeapi.REST(   "PKHR9AOB6FNQ8SUFY16X" ,
						"AbAIn4cBo8NdciOedKzNzpaqo5GVUzyf74QYnJqk",
						base_url = "https://paper-api.alpaca.markets" )

def get_data(symbol, start, end):

	# Historical Data with yfinance:
	#ticker = yf.Ticker(symbol)
	#data = ticker.history(period="max")
	#data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

	# Historical Data with alpaca API
	#data = api_.get_barset(symbol, timeframe='1D', start=start, end=end).df
	#data.columns = ['open', 'high', 'low', 'close', 'volume']

	# Historical Data with yahooquery
	ticker = Ticker(symbol, asynchronous=True)
	print(start, end)
	data = ticker.history(period='1d', interval='1d', start=start, end=end)
	data = data.droplevel(0)


	return data 



