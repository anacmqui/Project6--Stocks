import dash
from dash import html, dcc, callback, Input, Output
#from dash import Dash
#import dash_html_components as html
#import dash_core_components as dcc
#from dash.dependencies import Input, Output

import pandas as pd                                             # pip install pandas
import plotly.express as px
import pymongo                                                  # pip install "pymongo[srv]"
from bson.objectid import ObjectId
import dash_bootstrap_components as dbc

client = pymongo.MongoClient(
    "mongodb+srv://anaqui:wild2023@cluster0.hthr1sz.mongodb.net/test")

# Go into the database I created
db = client["final_project"]
# Go into one of my database's collection (table)
collection = db["users"]

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.MINTY])

app.layout = html.Div([
    html.H1('Web Application connected to a Live Database', style={'textAlign': 'center'}),
    # interval activated once/week or when page refreshed
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div(id='mongo-datatable', children=[]),
])

# Display Datatable with data from Mongo database
@app.callback(Output('mongo-datatable', component_property='children'),
              Input('interval_db', component_property='n_intervals')
              )
def populate_datatable(n_intervals):
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    # Convert id from ObjectId to string so it can be read by DataTable
    df['_id'] = df['_id'].astype(str)
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='our-table',
            data=df.to_dict('records'),
            columns=[{'id': p, 'name': p, 'editable': False} if p == '_id'
                     else {'id': p, 'name': p, 'editable': True}
                     for p in df],
        ),
    ]

if __name__ == '__main__':
	app.run_server(debug=True)
