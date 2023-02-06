import dash
from dash import html, dcc, callback, Input, Output, dash_table, State
from dash import Dash
import pandas as pd                                             # pip install pandas
import plotly.express as px
import pymongo                                                  # pip install "pymongo[srv]"
from bson.objectid import ObjectId
import dash_bootstrap_components as dbc
from pymongo import MongoClient 

#link = 'mongodb+srv://AnaQuint:anaquint@cluster0.rjc0cp4.mongodb.net/?retryWrites=true&w=majority'
#client = MongoClient(link)
#print(client.FinAna.transaction.find()[0])


client = pymongo.MongoClient("mongodb+srv://ana3:wild@cluster1.vd2kmxj.mongodb.net/?retryWrites=true&w=majority")
#client = MongoClient(link)

db = client['project6']
accounts = db['accounts']
transactions = db['transactions']
users = db['users']
#print(users.find()[0])

df = pd.DataFrame(list(accounts.find()))
df['_id'] = df['_id'].astype(str)
#df['id_users'] = df['id_users'].astype(str)

app = dash.Dash(__name__)

app.layout = dbc.Container([
        dash_table.DataTable(
            id='my-table',
            columns=[{'name': 'User_id', 'id': '_id', 'type':'text'},
                    {'name': 'Surname', 'id': 'Surname', 'type':'text'},
                    {'name': 'First name', 'id': 'First_name', 'type':'text'},
                    {'name': 'Email', 'id': 'Email', 'type':'text'},
                    {'name': 'Date of birth', 'id': 'Date_birth', 'type':'datetime'},
                    {'name': 'Currency', 'id': 'Currency', 'type':'text'},
                    ],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_current=0,  # page number that user is on
            page_size=6,  # number of rows visible per page
            style_cell={'textAlign': 'left', 'minWidth': '100px',
                        'width': '100px', 'maxWidth': '100px'},
                       )
                    ])
                    

if __name__ == '__main__':
    app.run_server(debug=True)