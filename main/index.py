import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from pages import test

server = app.server

app.title = "CandleDash"
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
     html.Nav(className = "nav nav-pills", children=[
                                                    html.A('LINK1', className="nav-item nav-link btn"),
                                                    html.A('LINK2', className="nav-item nav-link btn") 
                                                    ]),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return test.layout
    
if __name__ == '__main__':
    app.run_server(debug=True)
