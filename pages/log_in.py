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
'''
email_input = html.Div([dbc.Label("Email", html_for="example-email"),
                        dbc.Input(type="email", id="example-email", placeholder="Enter email"),
                        ],
                        className="mb-3",
                        )

password_input = html.Div([
                        dbc.Label("Password", html_for="example-password"),
                        dbc.Input(type="password", id="example-password", placeholder="Enter password")
                            ],
                    className="mb-3",
                )
'''


account_input = html.Div([
                        dbc.Label("Your account number", html_for="example-id"),
                        dbc.Input(type="id", id="example-id", placeholder="Enter account number")
                            ],
                    className="mb-3",
                )

stock_input = html.Div([dbc.Label("Type stock:", html_for="example-email"),
                        dbc.Input(type="stock", id="example-stock", placeholder="Enter stock ticker"),
                        ],
                        className="mb-3",
                        )

price_input = html.Div([dbc.Label("Type the price:", html_for="example-price"),
                        dbc.Input(type="price", id="example-price", placeholder="Enter stock price"),
                        ],
                        className="mb-3",
                        )

quantity_input = html.Div([dbc.Label("How many stocks:", html_for="example-quantity"),
                        dbc.Input(type="quantity", id="example-quantity", placeholder="Enter quantity"),
                        ],
                        className="mb-3",
                        )

#form1 = dbc.Form([account_input, stock_input, price_input, quantity_input])
form1 = dbc.Form([account_input, stock_input, price_input, quantity_input])
button1 = dbc.Button("Buy/Sell")
output_container = html.Div(className="mt-4")

#stock_input = html.Div([dbc.Label("Select a company", html_for="example-stock"),
 #                       dcc.Dropdown(options = dropdown_stock, value = 1, id = 'stocks-dropdown', placeholder = 'Press/type here'),
  #                      ],
   #                     className="mb-3",
    #                    )

def make_card(df=df_stocks_feb.to_dict('records')):
    company = df["Name"]
    price = df["Close"]
    logo = df["end_url"]
    ticker = df["Symbol"]
    print(logo)
    return dbc.Card(
        html.Div(
            [html.Img(src=f'https://app.outboundsales.io/api/logo/apple.com', height=35, className="me-1"),
            html.H4(company),
            html.H5(ticker),
            html.H5(price),
            ],
            #className=f"border-{color} border-start border-5",
                ),
                className="text-center text-nowrap my-2 p-2",
            )
    


cards = html.Div(id = 'my-card')

dash.register_page(__name__, path='/login')

layout = html.Div([
            dbc.Row(children = [
                    html.H1(
                     children = ['Build your portfolio'], style={'textAlign':'center', "padding": "2rem 1rem", 'color':'#000000'}
                     ), ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select a company", html_for="example-stock"),
                    dcc.Dropdown(options = dropdown_stock, value=[1], id = 'stocks-dropdown', placeholder = 'Press/type here',
                                    style={'color':'#000000'}),
                    ], width=3),
                    ]),
            dbc.Row([
                dbc.Col([cards
                    ], width=3),
                    ]),
            dbc.Row([
                dbc.Col([dbc.Button("Buy/Sell here",
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
    dff = df_stocks_feb.copy()
    print(stock)
    dff = dff[(dff['Name']==stock)]
    #dff = dff.to_dict('records')
    print(dff)
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
     Input(form1, "n_clicks"),
     State("example-id", "value"),
     State("example-stock", "value"),
     State("example-price", "value"),
     State("example-quantity", "value"),
     prevent_initial_call=True)
def portf(account, stock, price, quantity,_):
        db.transactions.insertOne([{ "id_account" : str(account),
                                "Date" : datetime.today(),
                                'Symbol' : str(stock),
                                "Price_per_share" : float(price),
                                'Quantity' : int(quantity),},
                                ])
        return 'Done!'                     
#def message(_):
 #   return 'Done!'
