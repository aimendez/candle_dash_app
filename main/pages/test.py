import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app


layout = html.Div([
    dbc.Card([
	    dbc.Row(html.H1("This is a test"),justify="center",className="title"),
	    dbc.Row(html.H3("Los landau son lo maximo"),justify="center",className="title"),
	],className="CartaTot",style={"min-height": "0px"}),
])