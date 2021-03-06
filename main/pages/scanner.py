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
                            value = 'AAPL'
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
                            style = {'fontSize':14}
                            )


bool_switch1 = daq.BooleanSwitch(
                                id='linear_plot_switch',
                                on=False,
                                color = '#3498db'
                                )
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# LAYOUT CARDS

card_header_dash = html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                        html.H5("CANDLE SCANNER", className="card-title", style={'textAlign':"center", 'font-weight': 'bold'}),
                        html.P("brief description of the dash", className="card-text", style={'textAlign':"center"}),
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
                        html.H5('Ticker', id='symbol_name_card', className="card-title"),
                        html.H6('Company Name', id='symbol_name_card2', className="card-text text-muted"),
                    ]
            ),
        className="card bg-light mt-4 mr-4"
        )
    ]
)

card2 =  html.Div( 
    [
        dbc.Card( 
                dbc.CardBody(
                    [
                        html.H5('Exchange', id = 'exchange_card', className="card-title"),
                        html.H6('Class', id = 'class_card', className="card-text text-muted"),
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
                        html.H5('Price' , id = 'close_price_card', className="card-title"),
                        html.Pre( html.H6('---  (---%)' , id = 'price_diff_card', className="card-text"), className = 'mb-0' ),
                    ]
            ),
        className="card bg-light  mt-4 mr-4"
        )
    ]
)



card_plot = html.Div(
    [
        dbc.Card([
            dbc.CardBody(
                [   
                    html.Div( [
                                html.Div('Line Plot', className='col-sm-0 ml-4', style={'marginLeft':'10rem'}),
                                html.Div(bool_switch1, className='col-sm-1'),
                                 
                             ], className='row justify-content-end' ),
                    html.Div(dcc.Graph(id = 'ohlc_plot', style={'marginTop':'1.5rem'})),
                ]
            ),
        ], className="card bg-light mr-4 mt-4"
        )
    ]
)


card_options =  html.Div( 
    [
        dbc.Card( [
                        dbc.CardHeader("OPTIONS"),
        
                        dbc.CardBody(
                            [
                                #html.H5("OPTIONS", className="card-title"),
                                html.H6( "Select Ticker Symbol", className="card-text mt-1"),
                                html.Div(dropdown_assets),
                                html.H6( "Select Candlestick Pattern(s)", className="card-text mt-4"),
                                html.Div( [ html.Div(dropdown_patterns,className='col-12 m4',)],className='row' ),
                                html.H6( "Pick Date Range", className="card-text mt-4"),
                                html.Div( [html.Div(date_picker, className='col-8'),  
                                           html.Div( html.Button('SCAN', id='scan-button', style={'height':'40px', 'width':'100px'}, className='btn btn-info'), className='col-4')
                                           ], className='row'),
                               # html.Div( html.Button('SCAN', id='scan-button', className='col-2 mr-4 mt-4 mb-1') )
        
                            ]
                        ),
                ],className="card bg-light ml-4 mt-4")
    ]
)

card_patterns =  html.Div( 
    [
        dbc.Card( [
        
                        dbc.CardHeader("CANDLESTICK PATTERNS"),
                        html.Div(id='pattern_description_id')#, style={'width':'30rem'})
        
               ],className="card bg-light ml-4 mt-4 mb-5")#, style={'height':'16.2rem'} )
    ]
)



#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# LAYOUT 

layout = html.Div([ 

    dbc.Row([ 
                dbc.Col([
                    (card_header_dash),
                 ])
            ]),

    dbc.Row([ 
                dbc.Col( [
                    (card_options),
                    (card_patterns)
                    ], width= 3 ),

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
                    ], width = 9 )

            ])
])

#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
# CALLBACKS 


# plot and company info
@app.callback( [ Output('ohlc_plot', 'figure'),
                 Output('symbol_name_card', 'children'),
                 Output('symbol_name_card2', 'children'),
                 Output('close_price_card', 'children'),
                 Output('price_diff_card', 'children'),
                 Output('price_diff_card', 'style'),
                 Output('exchange_card', 'children'),
                 Output('class_card', 'children'),


                ],              

               [Input('dropdown_assets', 'value'),
                Input('date-picker', 'start_date'),
                Input('date-picker', 'end_date'),
                Input('linear_plot_switch', 'on'),
                Input('scan-button', 'n_clicks')
               ], 

               [State('dropdown_patterns', 'value')]
             )
def Candlestick_plot(symbol, start_date, end_date, plot_switch, n_clicks, pattern_options):
    if symbol != None:
        #------------------ NAME CARD ------------------------#
        name = df_assets[df_assets['symbol'] == symbol].name
        class_ = str(df_assets[df_assets['symbol'] == symbol]['class'].values[0]).replace('_', ' ').upper()
        exchange = df_assets[df_assets['symbol'] == symbol]['exchange'].values[0]

        #------------------- DF -------------------------------#
        start_date = start_date.split('T')[0]
        df = utils.get_data(symbol, start_date, end_date)
        if len(df) == 0:
            color = {'color':'black'} 
            return [ go.Figure(), symbol, name, '---', '---  (---%)', color, '---',  '---'  ]

        # exception if date does not match history
        try:
            df = df.loc[start_date:end_date, :]
        except:
            df = df  

        #------------------ PRICE CARD ------------------------#
        last_close = str( round(df.close[-1], 2) ) + ' USD'
        last_diff = round(df.close[-1] - df.close[-2] , 2)
        last_pct = round( (df.close[-1] - df.close[-2])/df.close[-1] *100 ,2 )
        pct_change = str(last_diff) + f' USD (+{last_pct}%)' if last_pct>0 else str(last_diff) + f' USD ({last_pct}%)'
        color = {'color':'green'}  if last_pct>0 else {'color':'red'}

        #------------------ PRICE CHART CARD ------------------------#
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        if plot_switch == False:
            trace = go.Candlestick( x = df.index ,
                                    open = df.open,
                                    high = df.high,
                                    low = df.low,
                                    close = df.close,
                                    showlegend=False,
                                    name = 'OHLC'
                                    )

            title_chart = symbol + ' - Candlestick Chart'
            yaxis_title = 'Price'
        else:
            trace = go.Scatter( x = df.index ,
                                y = df.close,
                                showlegend=False,
                                name = 'CLOSE'
                                
                                )

            title_chart = symbol + ' - Close Price Line Chart'
            yaxis_title = 'Close Price'

        fig.add_trace(trace, secondary_y=False)
        #------------------ VOLUME CHART CARD ------------------------#
        volume_trace = go.Bar(x=df.index,
                              y=df.volume,
                              showlegend=False,
                              marker=dict(opacity=0.1, color='#3498db'),
                              name = 'VOL'
                              )

        fig.add_trace(volume_trace, secondary_y=True)
        #fig.update_yaxes(title_text="Volume", secondary_y=True)
        fig.update_yaxes(showticklabels=False, secondary_y=True)


        #------------------LAYOUT ------------------------#

        layout = go.Layout( title = title_chart,
                            xaxis = {'title' : 'Date', 'showgrid':False, 'type':'category'},
                            yaxis = {'title': yaxis_title, 'showgrid':False, 'range': ( df.low.min(), df.high.max())},
                            #yaxis2 = {'scaleanchor':"y2",'scaleratio':0.001},
                            xaxis_rangeslider_visible = False,
                            #plot_bgcolor = '#FFFFFF',
                            plot_bgcolor='rgba(0,0,0,0)',
                            #autosize=False,
                            #height=478,
                            margin=go.layout.Margin( r = 0 ),
                            paper_bgcolor='rgba(0,0,0,0)',
                         )
        fig.update_layout(layout)

        #----------------- PATTERN CHART --------------------#
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'scan-button' in changed_id and pattern_options!=None:
        #if n_clicks==1 and pattern_list!=None:
            if len(pattern_options)!=0:
                #find pattern and add to figure
                for pattern in pattern_options:
                    pattern_func = abstract.Function(pattern)
                    pattern_df = pattern_func(df.open, df.high, df.low, df.close) 
                    pattern_mask = [True if idx_tmp != 0 else False for idx_tmp in pattern_df]
                    #pattern_idx = np.nonzero( np.array(pattern_df) )
                    trace_pattern = go.Scatter( x = df.index[pattern_mask],
                                                y = df.high[pattern_mask] + abs( df.open[pattern_mask] - df.close[pattern_mask] ),
                                                name = pattern_list.pattern_list[pattern] ,
                                                mode='markers',
                                                marker=dict(
                                                            size = 15,
                                                            color='black',
                                                            symbol = 'arrow-down'
                                                            ),
                                                showlegend=False,
                                                )
                    fig.add_trace(trace_pattern)
            fig.update_layout(legend=dict(
                                            orientation="h",
                                            yanchor="bottom",
                                            y=-1,
                                            xanchor="left",
                                            x=0
                                        ))



               

        return [fig,
                symbol,
                name,
                last_close, 
                pct_change, 
                color, 
                'Exchange: '+ str(exchange) , 
                class_, 
                ] 

    else:
        return no_update

# callback for pattern card images
@app.callback( [ 
                 Output('pattern_description_id', 'children'),
                ],             

               [
                Input('scan-button', 'n_clicks')
               ], 

               [State('dropdown_patterns', 'value')]
             )
def candlestick_images(n_clicks, pattern_options):
    img_dict = pattern_list.pattern_img
    names_dict = pattern_list.pattern_list

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'scan-button' in changed_id and pattern_options!=None:
        if len(pattern_options)!=0:
            tabs = [] 
            for i in range( len(pattern_options) ):
                # bull/bear
                if len(img_dict[pattern_options[i]]) > 1:
                    direction = img_dict[pattern_options[i]][1]
                    color1 = 'success' if direction == 'bullish' or direction == 'up trend' else 'danger' if direction == 'bearish' or direction == 'down trend' else 'warning'

                    strength = img_dict[pattern_options[i]][2]
                    color2 = 'danger' if strength == 'strong' else 'warning' if strength == 'reliable' else 'secondary'

                    indicator = img_dict[pattern_options[i]][3]
                    color3 = 'danger' if indicator == 'reversal' else 'warning' if indicator == 'consolidation' else 'success'
                else:
                    direction = '' 
                    strength = ''
                    indicator = ''


                try:
                    split = direction.split('/')
                    split_c1 = 'success' if split[0] == 'bullish' or split[0] == 'up trend' else 'danger' if split[0] == 'bearish' or split[0] == 'down trend' else 'warning'
                    split_c2 = 'success' if split[1] == 'bullish' or split[1] == 'up trend' else 'danger' if split[1] == 'bearish' or split[1] == 'down trend' else 'warning'

                    tab_tmp = dcc.Tab( label = names_dict[pattern_options[i]] , 
                                       children = [  html.Div([
                                                                 html.Div(html.Img(src= img_dict[pattern_options[i]][0],style={'height':'90%', 'width':'70%'}), className='col ml-4' ),
                                                                 html.Div([
                                                                    html.H6(names_dict[pattern_options[i]], style = {'fontSize':'5'}, className = 'ml-0 mt-0 row'),
                                                                    html.Div( [dbc.Badge(split[0], pill=True, color=split_c1,  style={'width':'4.7rem'} ), 
                                                                               dbc.Badge( split[1], pill=True, color=split_c2, className="ml-2", style={'width':'4.7rem'}  )
                                                                               ], className= 'ml-0 mt-4 row'),
                                                                    html.Div( [ dbc.Badge(strength, pill=True, color=color1,  style={'width':'10rem'})], className="ml-0 mt-2 row"),
                                                                    html.Div( [ dbc.Badge(indicator, pill=True, color=color1, style={'width':'10rem'})], className="ml-0 mt-2 row"),
                                                                    ], className='col')
                                                               ], className = 'row mt-4 mb-2'
                                                      )
                                                ],
                                    style={'padding':'0','line-height': '3v'}, selected_style={'padding': '0','line-height': '3v', 'backgroundColor': '#3498db' , 'color':'white'}
                                    )
                except:
                    tab_tmp = dcc.Tab( label = names_dict[pattern_options[i]] , 
                                       children = [  html.Div([
                                                                 html.Div(html.Img(src= img_dict[pattern_options[i]][0],style={'height':'90%', 'width':'70%'}), className='col ml-4' ),
                                                                 html.Div([
                                                                    html.H6(names_dict[pattern_options[i]], style = {'fontSize':'5'}, className = 'ml-0 mt-0 row'),
                                                                    html.Div(dbc.Badge(direction, pill=True, color=color1, style={'width':'10rem'}) ,className="ml-0 mt-4 row"),
                                                                    html.Div(dbc.Badge(strength, pill=True,  color=color1, style={'width':'10rem'}), className="ml-0 mt-2 row"),
                                                                    html.Div(dbc.Badge(indicator, pill=True, color=color1, style={'width':'10rem'}), className="ml-0 mt-2 row"),
                                                                    ], className='col')
                                                               ], className = 'row mt-4 mb-2'
                                                      )
                                                ],
                                    style={'padding':'0','line-height': '3v'}, selected_style={'padding': '0','line-height': '3v',  'backgroundColor': '#3498db' , 'color':'white'}
                                    )
                tabs.append(tab_tmp)
            tabs_card = dcc.Tabs( value = 'tab-1', 
                                  children = tabs,
                                  style={
                                        'font-size': '70%',
                                        'height': '3v'
                                         } )

            return [tabs_card]
        else:
            return [ '' ]
    else:
        return no_update 
