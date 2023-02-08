import dash
from dash import html, dcc, callback, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pymongo import MongoClient
import pymongo 
import pprint
import json
from bson import json_util, ObjectId

client = pymongo.MongoClient("mongodb+srv://ana3:wild@cluster1.vd2kmxj.mongodb.net/?retryWrites=true&w=majority")
#client = MongoClient(link)

db = client['project6']
accounts = db['accounts']
transactions = db['transactions']
users = db['users']

DATATABLE_COLUMNS = ['_id','id_account', 'Date', 'Symbol', 'Price_per_share', 'Quantity']
FIND_FIELDS = {k: 1 for k in DATATABLE_COLUMNS}
FIND_FIELDS['_id'] = 0

#print(db.users.find({})[0])
user1 = db.users.find({})[0]
user_docs = list(db.users.find({}))
#print('user_docs',user_docs )
accounts_docs = db.accounts.find({})

def full_name(doc):
    return doc['First_name']+' '+ doc['Surname']

#print(list(map(full_name, db.users.find({}))))

#dropdown_index_user = list(map(full_name, db.users.find({})))

#print(dropdown_index_user)
#print(accounts_docs[0]['_id'])
#print(db.transactions.find({'id_account':'63e1264fdfd5c71ad333973a'})[0])

#account_index_id = 
#print(accounts_docs[0]['_id'])


dash.register_page(__name__, path='/database')

layout = html.Div([
            dbc.Row(children = [
                    html.H1(
                     children = ['Database'], style={'textAlign':'center', "padding": "2rem 1rem", 'color':'#8B1A1A'}
                     ), ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select a user:", style={'font-weight': 'bold'}),
                    dbc.Select(
                                options=[
                                {"label": "Ana Quintino", "value": 0},
                                {"label": "Cristina Zappullo", "value": 1},
                                {"label": "Luisa Policarpo", "value": 2},
                                {"label": "Sebastião Oliveira", "value": 3},
                                        ],
                                value=0,
                                id="users-select",
                             ), 
                            ], width=3),
                    ]),
            dbc.Row([
                 dbc.Col([ ], width=3, style = {'height':'50px'}),
                    ]), 
            dbc.Row([
                dbc.Col([
                    dbc.Label("List of transactions:", style={'font-weight': 'bold'}),
                    dash_table.DataTable(
                        id='my-table',
                        columns = list(map(lambda col: {"name": col, "id": col} , DATATABLE_COLUMNS)),
                        #editable=True,
                        #row_deletable=True,
                        #filter_action="native",
                        #filter_options={"case": "sensitive"},
                        #sort_action="native",  # give user capability to sort columns
                        #sort_mode="single",  # sort across 'multi' or 'single' columns
                        #page_current=0,  # page number that user is on
                        #page_size=6,  # number of rows visible per page
                        #style_cell={'textAlign': 'left', 'minWidth': '100px',
                         #           'width': '100px', 'maxWidth': '100px'},
                            )
                ], width=10),
            ]),
            ])
            

@callback(
    Output(component_id = 'my-table', component_property = 'data'),
    Input(component_id = 'users-select', component_property = 'value'),
)
def update_table(user):
    user = int(user)
    user_index_id = user_docs[user]['_id']
    account_index_id = db.accounts.find_one({'id_users':user_index_id})['_id']
    transactions_user = list(db.transactions.find({'id_account':str(account_index_id)},
                                            {'_id':0, 'id_account':1, 'Date':1, 'Symbol':1, 
                                            'Price_per_share':1, 'Quantity':1}))
    return transactions_user
