import dash
import dash_bootstrap_components as dbc
import pandas as pd
import alpaca_trade_api as tradeapi 

api_ = tradeapi.REST(   "PKHR9AOB6FNQ8SUFY16X" ,
						"AbAIn4cBo8NdciOedKzNzpaqo5GVUzyf74QYnJqk",
						base_url = "https://paper-api.alpaca.markets" )
assets = api_.list_assets()
df_assets = pd.DataFrame.from_dict(
								   { 'symbol':  [ asset.symbol for asset in assets],
						 			 'name':[ asset.name for asset in assets],
						 			 'exchange':[ asset.exchange for asset in assets],
						 			 'status':[ asset.status for asset in assets],

						}).to_csv('./assets/asset_list.csv')

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY,dbc.themes.GRID])
server = app.server
app.layout