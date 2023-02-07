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

#print(db.users.find({})[0])
user1 = db.users.find({})[0]
user_docs = list(db.users.find({}))
print('user_docs',user_docs )
accounts_docs = db.accounts.find({})

def full_name(doc):
    return doc['First_name']+' '+ doc['Surname']

#print(list(map(full_name, db.users.find({}))))

dropdown_index_user = list(map(full_name, db.users.find({})))
#print(dropdown_index_user)
#print(accounts_docs[0]['_id'])
#print(db.transactions.find({'id_account':'63e1264fdfd5c71ad333973a'})[0])

#account_index_id = 
#print(accounts_docs[0]['_id'])

print('database.py')


dash.register_page(__name__, path='/database')

layout = html.Div([
            dbc.Row(children = [
                    html.H1(
                     children = ['Database'], style={'textAlign':'center', "padding": "2rem 1rem", 'color':'#8B1A1A'}
                     ), ]),
            dbc.Row([
                 dbc.Select(
                    options=[
                        {"label": "Ana Quintino", "value": 0},
                        {"label": "Cristina Zappullo", "value": 1},
                        {"label": "Luisa Policarpo", "value": 2},
                        {"label": "Sebastião Oliveira", "value": 3},
                    ],
                    value=0,
                    id="users-select",
                ),]),
            dbc.Row([
                    html.Div(
                        id = 'my-table'),
                        ]),
                #dash_table.DataTable(
                 #       id='my-table',
                  #      columns=[#{'name': 'Id', 'id': '_id'},
                   #         {'name': 'Account_id', 'id': 'id_account'},
                    #                {'name': 'Date', 'id': 'Date'},
                     #               {'name': 'Symbol', 'id': 'Symbol'},
                      #              {'name': 'Price per share', 'id': 'Price_per_share'},
                       #             {'name': 'Quantity', 'id': 'Quantity'},
                        #        ],)
            
                        #data = transactions.to_dict('records'),
                    
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
                ])
                    
            

@callback(
    Output(component_id = 'my-table', component_property = 'children'),
    Input(component_id = 'users-select', component_property = 'value'),
)
def update_table(user):
    #print('update_table')
    #print(type(user), user)
    user = int(user)
    user_index_id = user_docs[user]['_id']
    #print(type(user_index_id))
    account_index_id = db.accounts.find_one({'id_users':user_index_id})['_id']
    #print(account_index_id)
    transactions_user = list(db.transactions.find({'id_account':str(account_index_id)}))
    #print(transactions_user)
    return dash_table.DataTable(
                       # id='my-table',
                        columns=[{'name': 'Id', 'id': '_id'},
                            {'name': 'Account_id', 'id': 'id_account'},
                                    {'name': 'Date', 'id': 'Date'},
                                    {'name': 'Symbol', 'id': 'Symbol'},
                                    {'name': 'Price per share', 'id': 'Price_per_share'},
                                    {'name': 'Quantity', 'id': 'Quantity'},
                                ],
                        data = transactions_user)
