import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from pages import test, scanner, screener
import utils 

server = app.server

app.title = "CandleDash"
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
     html.Nav(className = "navbar navbar-expand-lg navbar-dark bg-dark", children=[
                                                    html.A('LANDAU DASH', className="nav-item nav-link btn"), 
                                                    html.A('Screener', className="nav-link btn", href = '/screener'),
                                                    html.A('Candle Scanner', className="nav-link btn", href = '/scanner'),
                                                    ]),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/scanner' or   pathname == '/' :
        return scanner.layout
    elif pathname == '/screener':
        return screener.layout
    else:
        return scanner.layout
    
if __name__ == '__main__':
    app.run_server(debug=True)
