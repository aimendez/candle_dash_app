import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

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






