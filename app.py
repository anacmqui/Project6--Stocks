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

link = 'mongodb+srv://AnaQuint:anaquint@cluster0.rjc0cp4.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(link)
# Go into the database I created
db = client["FinAna"]

# Go into one of my database's collection (table)
collection = db.transaction
#print(collection.find()[0])
df = pd.DataFrame(list(collection.find()))
#Drop the _id column generated automatically by Mongo
#df = df.iloc[:, 1:]

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([

    #html.Div(id='mongo-datatable'),
    dash_table.DataTable(
            id='my-table',
            columns=[{
                'name': x,
                'id': x,
            } for x in df.columns],
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
        ),

    # activated once/week or when page refreshed
    dcc.Interval(id='interval_db', interval=86400000 * 6, n_intervals=0),

    html.Button("Save to Mongo Database", id="save-it"),
    html.Button('Add Row', id='adding-rows-btn', n_clicks=0),

    html.Div(id="show-graphs", children=[]),
    html.Div(id="placeholder")

])




# Add new rows to DataTable ***********************************************
@app.callback(
    Output('my-table', 'data'),
    [Input('adding-rows-btn', 'n_clicks')],
    [State('my-table', 'data'),
     State('my-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the Mongo database ***************************
@app.callback(
    Output("placeholder", "children"),
    Input("save-it", "n_clicks"),
    State("my-table", "data"),
    prevent_initial_call=True
)
def save_data(n_clicks, data):
    dff = pd.DataFrame(data)
    collection.delete_many({})
    collection.insert_many(dff.to_dict('records'))
    return ""


# Create graphs from DataTable data ***************************************
@app.callback(
    Output('show-graphs', 'children'),
    Input('my-table', 'data')
)
def add_row(data):
    df_grpah = pd.DataFrame(data)
    fig_hist1 = px.histogram(df_grpah, x='age',color="animal")
    fig_hist2 = px.histogram(df_grpah, x="neutered")
    return [
        html.Div(children=[dcc.Graph(figure=fig_hist1)], className="six columns"),
        html.Div(children=[dcc.Graph(figure=fig_hist2)], className="six columns")
    ]


if __name__ == '__main__':
    app.run_server(debug=True)