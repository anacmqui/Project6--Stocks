import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/login')

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

form = dbc.Form([email_input, password_input])
button = dbc.Button("Enter your portfolio")
output_container = html.Div(className="mt-4")

layout = html.Div([
            dbc.Row(children = [
                    html.H1(
                     children = ['Build your portfolio'], style={'textAlign':'center', "padding": "2rem 1rem", 'color':'#8B1A1A'}
                     ), ]),
            dbc.Container([form, button, output_container], fluid=True)
                    ])