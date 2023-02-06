import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/')

df_states = pd.read_csv('https://raw.githubusercontent.com/anacmqui/Project6--Stocks/main/state_result.csv')

def us_map(df=df_states):
    fig = go.Figure(data=go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_states['Longitude'],
        lat = df_states['Latitude'],
        hovertext = df_states[['Headquarters', 'Name']],
        #mode = 'markers',
        marker = dict(
            size = df_states['Name'],
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
        )))
    fig.update_layout(
        #title = 'Most trafficked US airports<br>(Hover for airport names)',
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            showland = True,
            landcolor = "#B0B0B0",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )
    return fig


layout  =  html.Div([
            dbc.Row(children = [
                    html.H1(
                     children = ['S&P 500 Stock Market Overview'], style={'textAlign':'center', "padding": "2rem 1rem", 'color':'#8B1A1A'}
                     ), ]),
            dbc.Row(children = [
                    html.H2(
                     children = ['Where are these companies?'], style={'textAlign':'center'}
                     ), ]),
            dbc.Row([dcc.Graph(figure=us_map()),]),
            #dbc.Row([
             #   dbc.Col([
              #      html.H2('What is the distribution of the score?', style={'textAlign':'center', "padding": "2rem 1rem"}
               #             ),
                #     dcc.Graph(figure=points_dist()),
                 #    ], width=6),
                #dbc.Col([html.H2('Where are the wines with 100 points?', style={'textAlign':'center', "padding": "2rem 1rem"}
                 #    ),
                  #   dcc.Graph(figure=best_score()), 
                   #  ], width=6),     
                    #]),

            #dbc.Row([
                  #dbc.Col([ 
                   # dbc.Row([html.H1('What are the grapes with best score?', style={'textAlign':'center', "padding": "2rem 1rem"}
                    #    ),]),
                     #dbc.Row([dcc.Graph(figure=best_grapen())]), 
                  #], width= 6),
                  # dcc.Graph(figure=prevision_value()),
                 #dbc.Col([ 
                    #dbc.Row([html.H2('What are the top grapes with best score?', style={'textAlign':'center', "padding": "2rem 1rem"}
                     #   ),]),
                     #dbc.Row([dcc.Graph(figure=best_grape15())
                     #]),
                    #], width= 6),
                # ]),
              ])


