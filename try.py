import dash
from dash import html, dcc, callback, Input, Output, dash_table, State
from dash import Dash
#import dash_html_components as html
#import dash_core_components as dcc
#from dash.dependencies import Input, Output

import pandas as pd                                             # pip install pandas
import plotly.express as px
import pymongo                                                  # pip install "pymongo[srv]"
from bson.objectid import ObjectId
import dash_bootstrap_components as dbc
from pymongo import MongoClient 

#client = pymongo.MongoClient("mongodb+srv://ana2:wild@cluster0.hthr1sz.mongodb.net/?retryWrites=true&w=majority")
#link = 'mongodb+srv://AnaQuint:anaquint@cluster0.rjc0cp4.mongodb.net/?retryWrites=true&w=majority'
#client = MongoClient(link)
#print(client.FinAna.transaction.find())


client = pymongo.MongoClient("mongodb+srv://ana3:<password>@cluster1.vd2kmxj.mongodb.net/?retryWrites=true&w=majority")
#client = MongoClient(link)

db = client.project6
collection = db['accounts']
print(collection.find()[0])

#print(client.server_info())
# Go into the database I created
#db = client["final_project"]
# Go into one of my database's collection (table)
#collection = db.transactions
#print(collection.find({})[0])

#df = pd.DataFrame(list(collection.find()))