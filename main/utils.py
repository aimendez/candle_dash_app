import yfinance  as yf
import pandas as pd 

def get_data(symbol):
	ticker = yf.Ticker(symbol)
	hist = ticker.history(period="max")
	data = hist[['Open', 'High', 'Low', 'Close', 'Volume']]
	data.columns = [ col_name.lower() for col_name in data.columns]
	return data 
