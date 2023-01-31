import dash                                                     # pip install dash  (2.1 or higher)
from dash import html, dcc, Input, Output, State, dash_table
import pandas as pd                                             # pip install pandas
import plotly.express as px
import pymongo                                                  # pip install "pymongo[srv]"
from bson.objectid import ObjectId
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.MINTY])



if __name__ == '__main__':
	app.run_server(debug=True)