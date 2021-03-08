import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
import json
from datetime import datetime , date
from assets import pattern_list 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Dropdown Menu for STOCK TICKERS



# dropdown menu for CANDLE PATTERNS
pattern_options = [{'label': v , 'value': k}   for k,v in pattern_list.pattern_list.items()]
dropdown_patterns = dcc.Dropdown(
                            id = 'dropdown_patterns',
                            options = pattern_options,
                            multi=True,
                            placeholder = 'Select Candlestick Pattern(s)',
                            )



# DatePicker for DF date range
date = datetime.date(datetime.now())
date_picker = dcc.DatePickerRange(
                            id='date-picker',
                            start_date= datetime(2020, 1, 1),
                            end_date = str(date),
                            )
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

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
                        html.H5("Card title", className="card-title"),
                        html.P( "this is a placeholder", className="card-text"),
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
                        html.Div( [ html.Div(dropdown_patterns,className='col-9 m4',), html.Button('SCAN', className='col-2 mr-0')],className='row' ),
                        html.Div(date_picker, className='mt-4')

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
                    html.H5("Here's a plot", className="card-title"),
                    html.P(
                        "this is a placeholder for plot",
                        className="card-text"),
                    dcc.Graph(id = 'ohlc_plot'),
                ]
            ),
        className="card bg-light mr-4 mt-4"
        )
    ]
)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#

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
                        dbc.Col(card1),
                        dbc.Col(card1)
                        ]),
                    dbc.Row(
                        dbc.Col(card_plot)
                        ),
                    ], width = 8 )

            ])
    ])

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#






