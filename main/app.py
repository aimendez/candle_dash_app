import dash
import dash_bootstrap_components as dbc
import pandas as pd
import alpaca_trade_api as tradeapi 
import utils 
import os

api_ = tradeapi.REST(  os.environ['ALPACA_KEY_ID'] ,
					   os.environ['ALPACA_SECRET_KEY'],
					   base_url = "https://paper-api.alpaca.markets" )

assets = api_.list_assets()
df_assets = pd.DataFrame(
						   { 'symbol':  [ asset.symbol for asset in assets if asset.tradable == True],
				 			 'name':[ asset.name for asset in assets if asset.tradable == True],
				 			 'exchange':[ asset.exchange for asset in assets if asset.tradable == True],
				 			 'status':[ asset.status for asset in assets if asset.tradable == True],
							}).sort_values('symbol').to_csv('./assets/asset_list.csv')

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY,dbc.themes.GRID])
server = app.server
app.layout