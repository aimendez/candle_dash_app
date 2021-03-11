import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import no_update

import plotly.graph_objs as go 
from plotly.subplots import make_subplots
import plotly.express as px


from app import app
import json
from datetime import datetime , date
from assets import pattern_list 
import pandas as pd
import utils 
import yfinance  as yf


#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# DASH COMPONENTS

# Dropdown Menu for STOCK TICKERS
df_assets = pd.read_csv( './assets/asset_list.csv').dropna()
asset_options = [{'label': row['symbol']+' ('+ str(row['name'])[:50]+'... )' , 'value': row['symbol'] }  if len(str(row['name'])) >=30 else {'label': row['symbol']+' ('+ str(row['name'])+')' , 'value': row['symbol']} for idx,row in df_assets.iterrows() ] 
dropdown_assets = dcc.Dropdown(
                            id = 'dropdown_assets',
                            options = asset_options,
                            placeholder = 'Select Company Symbol',
                            )

# Dropdown menu for CANDLE PATTERNS
pattern_options = [{'label': v , 'value': k}   for k,v in pattern_list.pattern_list.items()]
dropdown_patterns = dcc.Dropdown(
                            id = 'dropdown_patterns',
                            options = pattern_options,
                            multi=True,
                            placeholder = 'Select Candlestick Pattern(s)',
                            )

# DatePicker for DATE RANGE
date_picker = dcc.DatePickerRange(
                            id='date-picker',
                            start_date= datetime(2020, 1, 1),
                            end_date = str(datetime.date(datetime.now())),
                            )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# LAYOUT CARDS

card_header_dash = html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                        html.H5("LANDAU APP", className="card-title", style={'textAlign':"center"}),
                        html.P("this is a placeholder for a nice header", className="card-text", style={'textAlign':"center"}),
                    ]
            ),
        className="card bg-light ml-4 mt-4 mr-4"
        )
    ]
)

card1 =  html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                        html.H3(id='symbol_name_card', className="card-title"),
                        html.P(id='symbol_name_card2', className="card-text"),
                    ]
            ),
        className="card bg-light  mt-4 mr-4"
        )
    ]
)

card2 =  html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                        html.H5('', className="card-title"),
                        html.P('', className="card-text"),
                    ]
            ),
        className="card bg-light  mt-4 mr-4"
        )
    ]
)

card3 =  html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                        html.H5('', className="card-title"),
                        html.P('', className="card-text"),
                    ]
            ),
        className="card bg-light  mt-4 mr-4"
        )
    ]
)

card_options =  html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                        html.H5("Card title", className="card-title"),
                        html.P( "this is a placeholder for some options (sliders/calendar/etc)", className="card-text"),
                        html.Div(dropdown_assets),
                        html.Div( [ html.Div(dropdown_patterns,className='col-12 m4',)],className='row mt-4' ),
                        html.Div(date_picker, className='mt-4'),
                        html.Div( html.Button('SCAN', className='col-2 mr-4 mt-4') )

                    ]
            ),
        className="card bg-light ml-4 mt-4"
        )
    ]
)

card_plot = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id = 'ohlc_plot'),
                ]
            ),
        className="card bg-light mr-4 mt-4"
        )
    ]
)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# LAYOUT 

layout = html.Div([ 

    dbc.Row([ 
                dbc.Col([card_header_dash ], width= 12)
            ]),

    dbc.Row([ 
                dbc.Col( card_options, width=4 ),

                dbc.Col([  
                    dbc.Row( 
                        [
                        dbc.Col(card1),
                        dbc.Col(card2),
                        dbc.Col(card3)
                        ]),
                    dbc.Row(
                        dbc.Col(card_plot)
                        ),
                    ], width = 8 )

            ])
])

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# CALLBACKS 


# plot and company info
@app.callback( [ Output('ohlc_plot', 'figure'),
                 Output('symbol_name_card', 'children'),
                 Output('symbol_name_card2', 'children')
                ],              
               [Input('dropdown_assets', 'value'),
                Input('date-picker', 'start_date'),
                Input('date-picker', 'end_date')
               ]
             )
def Candlestick_plot(symbol, start_date, end_date):
    if symbol != None:
        start_date = start_date.split('T')[0]
        df = utils.get_data(symbol, start_date, end_date)
        name = df_assets[df_assets['symbol'] == symbol].name

        # exception if date does not match history
        try:
            df = df.loc[start_date:end_date, :]
        except:
            df = df  

        # fig of ohlc plot
        fig = go.Figure()
        trace = go.Candlestick( x = df.index ,
                                open = df.open,
                                high = df.high,
                                low = df.low,
                                close = df.close,
                                )
        layout = go.Layout( title = symbol + ' - Candlestick Chart',
                            xaxis = {'title' : 'Date', 'showgrid':False, 'type':'category'},
                            yaxis = {'title': 'Price', 'showgrid':False},
                            xaxis_rangeslider_visible = False,
                            plot_bgcolor = '#FFFFFF',
                            autosize=False,
                        )
        fig.add_trace(trace)
        fig.update_layout(layout)

        return [fig, symbol, name ] 
    else:
        return no_update

