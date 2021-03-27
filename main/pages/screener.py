import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash import no_update
import dash

import plotly.graph_objs as go 
from plotly.subplots import make_subplots
import plotly.express as px

from talib import abstract


from app import app
import json
from datetime import datetime , date
from assets import pattern_list 
import pandas as pd
import numpy as np
import utils 
import yfinance  as yf


df_assets = pd.read_csv( './assets/asset_list.csv').dropna()
exchange_options = [ {'label':ex, 'value':ex} for ex in df_assets.exchange.unique() ]
dropdown_exchange = dcc.Dropdown(
                            id = 'dropdown_exchange',
                            options = exchange_options,
                            placeholder = 'Select Exchange',
                            #value = 'ALL'
                            )

# Dropdown menu for CANDLE PATTERNS
pattern_options = [ {'label': v , 'value': k}   for k,v in pattern_list.pattern_list.items() ]
pattern_options.append( {'label': 'COMPLETE SUMMARY' , 'value': 'ALL'} )
dropdown_patterns = dcc.Dropdown(
                            id = 'dropdown_patterns',
                            options = pattern_options,
                            #multi=True,
                            placeholder = 'Select Candlestick Pattern(s)',
                            value = 'ALL'
                            )


# Table 
table_header = [
    html.Thead(html.Tr([
    			html.Th("Symbol"), 
    			html.Th("Name"),
    			html.Th("Last Update"),
    			html.Th("Close"),
    			html.Th(" % "),
    			html.Th("Signal")
    			]))
]
table_body = [html.Tbody([])]
table = dbc.Table(table_header + table_body, bordered=True)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# LAYOUT CARDS

card_header_dash = html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                        html.H5("CANDLE SCREENER", className="card-title", style={'textAlign':"center", 'font-weight': 'bold'}),
                        html.P("brief description of the wea", className="card-text", style={'textAlign':"center"}),
                    ]
            ),
        className="card bg-light ml-4 mt-4 mr-4"
        )
    ]
)


card_table = html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                    	html.Div( [html.Div(dropdown_patterns, className='col-4'),  
                    			   html.Div(dropdown_exchange, className='col-4'),
                                   html.Div( html.Button('SCAN', id='scan-button', style={'height':'40px', 'width':'100px'}, className='btn btn-info'), className='col-4')
                                   ], className='row mb-4'),
                        html.Div(id = 'table-screener', children= table, className = 'mt-2')
                    ]
            ),
        className="card bg-light ml-4 mt-4 mr-4"
        )
    ]
)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# LAYOUT CARDS

layout = html.Div([ 

    dbc.Row([ 
                dbc.Col([
                    (card_header_dash),
                 ])
            ]),

    dbc.Row([ 
                dbc.Col([
                    (card_table),
                 ])
            ]),

])



#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# CALLBACKS



# plot and company info
@app.callback( [ Output('table-screener', 'children') ],
               [ Input('scan-button', 'n_clicks') ],
               [State('dropdown_patterns', 'value'), State('dropdown_exchange', 'value')],
             )
def Candlestick_plot(n_clicks, pattern, exchange):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'scan-button' in changed_id and pattern_options!=None:
		rows = []
		pattern_func = abstract.Function(pattern)
		df_assets_filtered = df_assets[ df_assets['exchange'] == exchange ]
		print(len(df_assets_filtered))
		for idx, row in df_assets_filtered.iterrows():
			symbol = row['symbol']
			df = utils.get_data(symbol)
			if len(df)!=0:
				print(symbol)
				pattern_df = pattern_func(df.open, df.high, df.low, df.close) 
				if pattern_df[-1] < 0:
					row_tmp = html.Tr([html.Td(symbol), html.Td(row['name']), html.Td( df.index[-1] ),  html.Td( df.loc[df.index[-1], 'close'] ), html.Td( np.nan ), html.Td( 'Bearish' )])
					rows.append(row_tmp)
				elif pattern_df[-1] > 0:
					row_tmp = html.Tr([html.Td(symbol), html.Td(row['name']), html.Td( df.index[-1] ),  html.Td( df.loc[df.index[-1], 'close'] ), html.Td( np.nan ), html.Td( 'Bullish' )])
					rows.append(row_tmp)
			else:
				continue

		table_body = [html.Tbody(rows)]
		table = dbc.Table(table_header + table_body, bordered=True)
		return [table]
	else:
		return no_update