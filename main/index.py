import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from pages import test, front_page
import utils 

server = app.server

app.title = "CandleDash"
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
     html.Nav(className = "navbar navbar-expand-lg navbar-dark bg-dark", children=[
                                                    html.A('LANDAU DASH', className="nav-item nav-link btn"), 
                                                    html.A('LINK1', className="nav-link btn"),
                                                    html.A('LINK2', className="nav-link btn") 
                                                    ]),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return front_page.layout
    
if __name__ == '__main__':
    app.run_server(debug=True)
