import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pymongo import MongoClient
import pymongo 
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://ana3:wild@cluster1.vd2kmxj.mongodb.net/?retryWrites=true&w=majority")
#client = MongoClient(link)

db = client['project6']
accounts = db['accounts']
transactions = db['transactions']
users = db['users']


df_stocks_feb = pd.read_csv('https://raw.githubusercontent.com/anacmqui/Project6--Stocks/main/df_result%20(1).csv')
df_stocks_feb = df_stocks_feb[['Symbol', 'Close', 'Name', 'Sector', 'url', 'Name_low2']]
df_stocks_feb['end_url'] = df_stocks_feb['Name_low2']+'.com'

dropdown_stock = df_stocks_feb['Name'].unique()


account_input = html.Div([
                        #dbc.Label("Fill in the info below", style={'font-weight': 'bold'}),
                        dbc.Label("Your account number", html_for="example-id"),
                        dbc.Input(type="id", id="example-id", placeholder="Enter account number")
                            ],
                    className="mb-3",
                )

stock_input = html.Div([dbc.Label("Which stock?", html_for="example-email"),
                        dbc.Input(type="stock", id="example-stock", placeholder="Enter stock ticker"),
                        ],
                        className="mb-3",
                        )

price_input = html.Div([dbc.Label("What is the price?", html_for="example-price"),
                        dbc.Input(type="price", id="example-price", placeholder="Enter stock price"),
                        ],
                        className="mb-3",
                        )

quantity_input = html.Div([dbc.Label("How many stocks?", html_for="example-quantity"),
                        dbc.Input(type="quantity", id="example-quantity", placeholder="Enter quantity"),
                        ],
                        className="mb-3",
                        )

#form1 = dbc.Form([account_input, stock_input, price_input, quantity_input])
form1 = dbc.Form([account_input, stock_input, price_input, quantity_input])
button1 = dbc.Button("Buy/Sell")
output_container = html.Div(className="mt-4")


def make_card(df=df_stocks_feb):
    company = df["Name"]
    price = df["Close"]
    logo = df["end_url"]
    ticker = df["Symbol"]
    #print(logo)
    return dbc.Card(html.Div(
                [dbc.CardImg(src=f'https://app.outboundsales.io/api/logo/{logo.iloc[0]}', className="me-1", top=True, 
                            style={"width": "5rem", 'height':'5rem'}),
                    dbc.CardBody([
                            html.H4(company, style={'textAlign':'center'}),
                            html.H5(ticker, style={'textAlign':'center'}),
                            html.H5(f'${round(price.iloc[0],2)}', style={'textAlign':'center'}),
                                ]),
                                ],
                        #style={"width": "18rem"},
                        
                        ), style={'textAlign':'center'})
    '''
    dbc.Card(
        html.Div(
            [html.Img(src=f'https://app.outboundsales.io/api/logo/{logo.iloc[0]}', height=35, className="me-1"),
            html.H1(),
            html.H4(company),
            html.H5(ticker),
            html.H5(f'${round(price.iloc[0],2)}'),
            ],
                ),
                className="text-center text-nowrap my-2 p-2",
                style={"width": "18rem"}
            )
    '''


cards = html.Div(id = 'my-card')

dash.register_page(__name__, path='/login')

layout = html.Div([
            dbc.Row(children = [
                    html.H1(
                     children = ['Build your portfolio'], style={'textAlign':'center', "padding": "2rem 1rem", 'color':'#104E8B', 'font-weight': 'bold'}
                     ), ]),
            dbc.Row(children = [
                    html.H3(
                     children = ['Step 1 - Check the stock price today'], style={'textAlign':'left', "padding": "2rem 1rem", 'color':'#104E8B'}
                     ), ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select a company", html_for="example-stock"),
                    dcc.Dropdown(options = dropdown_stock, value=[1], id = 'stocks-dropdown', placeholder = 'Press/type here',
                                    style={'color':'#104E8B'}),
                    ], width=3),
                    ]),
            dbc.Row([dbc.Label(" "),
                    ]),
            dbc.Row([
                dbc.Col([
                    ], width=4),
                dbc.Col([cards
                    ], width=3),
                dbc.Col([
                    ], width=3),
                    ]),
            dbc.Row([dbc.Label(" s ",style={'color':'#F8F8FF'} ),
                    ]),
            dbc.Row([dbc.Label(" "),
                        html.Hr(),
                    ]),
            dbc.Row(children = [
                    html.H3(
                     children = ['Step 2 - Buy/sell the stock'], style={'textAlign':'left', "padding": "2rem 1rem", 'color':'#104E8B'}
                     ), ]),
            dbc.Row([
                dbc.Col([dbc.Button("Add to portfolio",
                                    id="collapse-button",
                                    className="mb-3",
                                    color="primary",
                                    n_clicks=0,
                                    ),
                        dbc.Collapse(
                            dbc.Container([form1, button1, output_container], fluid=True),
                            id="collapse",
                            is_open=False,
                                    ),
                    ], width=3),
                    ]),
                ])

@callback(
    Output('my-card', "children"), 
    Input('stocks-dropdown', "value"))
def update_cards(stock):
    #dff = df_stocks_feb.copy()
    #print(stock)
    print(type(df_stocks_feb['Name'].iloc[0]))
    dff = df_stocks_feb[df_stocks_feb['Name'].str.contains(stock)]
    #print(dff)
    return make_card(dff)

@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
     Output(output_container, "children"),
     Input(button1, "n_clicks"),
     State("example-id", "value"),
     State("example-stock", "value"),
     State("example-price", "value"),
     State("example-quantity", "value"),
     prevent_initial_call=True)
def portf(_, account, stock, price, quantity):
        db.transactions.insert_many([{ "id_account" : str(account),
                                "Date" : datetime.today(),
                                'Symbol' : str(stock),
                                "Price_per_share" : float(price),
                                'Quantity' : int(quantity),},
                                ])
        return 'Done!'                     
#def message(_):
 #   return 'Done!'
