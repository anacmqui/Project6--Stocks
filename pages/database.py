import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/database')

layout = html.Div(children=[])