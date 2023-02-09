import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime as dt
from datetime import datetime

dash.register_page(__name__, path='/')

df_states = pd.read_csv('https://raw.githubusercontent.com/anacmqui/Project6--Stocks/main/state_result.csv')
df_sectors = pd.read_csv('https://raw.githubusercontent.com/anacmqui/Project6--Stocks/main/df_sectors%20(1).csv')
df_stocks = pd.read_csv('https://raw.githubusercontent.com/anacmqui/Project6--Stocks/main/df_stocks_final.csv')
df_comp_logo = pd.read_csv('https://raw.githubusercontent.com/anacmqui/Project6--Stocks/main/df_company.csv')

print(type(df_stocks['Date'][0]))
df_stocks['Date'] = pd.to_datetime(df_stocks['Date'])
#df_stocks.set_index('Date', inplace=True)

df_sectors = df_sectors[df_sectors['Sector']!='Index']

dropdown_sectors = df_sectors['Sector'].unique()
dropdown_stocks = df_stocks['Name'].unique()

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
            color ='#00BFFF',
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

def sectors_line(df=df_sectors):
    return px.line(df, x='Date', y="Close", color='Sector')

def stocks_line(df=df_stocks):
    return px.line(df, x='Date', y="Close", color='Name', hover_data=['Sector'])

layout  =  html.Div([
            dbc.Row(children = [
                    html.H1(
                     children = ['S&P 500 Stock Market Overview'], style={'textAlign':'center', "padding": "2rem 1rem", 'color':'#00BFFF'}
                     ), ]),
            dbc.Row(children = [
                    html.H2(
                     children = ['Where are these companies?'], style={'textAlign':'center'}
                     ), ]),
            dbc.Row([dcc.Graph(figure=us_map()),]),
            dbc.Row([
                    html.H2('Explore per industry', style={'textAlign':'center', "padding": "2rem 1rem"}
                            ),
                    html.Label(['Select an industry:'],
                    style={'font-weight': 'bold'}),
                    html.P(),   
                    dcc.Dropdown(options = dropdown_sectors, value = [1],multi=True, id = 'sectors-dropdown', placeholder = 'Press/type here'),
                    dcc.Graph(figure=sectors_line(), id='line-graph'),
                    ]),
                #dbc.Col([html.H2('Where are the wines with 100 points?', style={'textAlign':'center', "padding": "2rem 1rem"}
                 #    ),
                  #   dcc.Graph(figure=best_score()), 
                   #  ], width=6),     
                    #]),

            dbc.Row([
                    html.H2('Explore per company', style={'textAlign':'center', "padding": "2rem 1rem"}
                            ),]),
            dbc.Row([
                    dbc.Col([
                        html.Label(['Select a stock:'], style={'font-weight': 'bold'}),
                        html.P(),
                         ], width = 6),
                    dbc.Col([
                        html.Label(['Select a date range:'], style={'font-weight': 'bold'}),
                        html.P(),
                         ], width = 6),
                    ]),
            dbc.Row([
                    dbc.Col([
                            dcc.Dropdown(options = dropdown_stocks, value = [1],multi=True, id = 'stocks-dropdown', placeholder = 'Type here'),]
                        ,width = 6),
                    dbc.Col([dcc.DatePickerRange(
                            #month_format='M-D-Y-Q',
                            #end_date_placeholder_text='M-D-Y-Q',
                            #start_date=date(2015, 1, 1), 
                            clearable=True,  # whether or not the user can clear the dropdown
                            number_of_months_shown=1,  # number of months shown when calendar is open
                            min_date_allowed=dt(2015, 1, 1),  # minimum date allowed on the DatePickerRange component
                            max_date_allowed=dt(2023, 2, 6),  # maximum date allowed on the DatePickerRange component
                            initial_visible_month=dt(2015, 1, 1),  # the month initially presented when the user opens the calendar
                            start_date=dt(2015, 1, 1).date(),
                            end_date=dt(2023, 2, 6).date(),
                            #display_format='%B %d %Y',
                            id='date-range'
                            )
                        ], width = 6),
                    ]),
            dbc.Row([
                    dcc.Graph(figure=stocks_line(), id='stock-graph'),
                     ]),
                  # dcc.Graph(figure=prevision_value()),
                   # ])
                 #dbc.Col([ 
                  #  dbc.Row([html.H2('What are the top grapes with best score?', style={'textAlign':'center', "padding": "2rem 1rem"}
                   #     ),]),
                    # dbc.Row([dcc.Graph(figure=best_grape15())
                     #]),
                    #], width= 6),
                     #   ]),
                    ])

@callback(
    Output(component_id = 'line-graph', component_property = 'figure'),
    Input(component_id = 'sectors-dropdown', component_property = 'value'),
)

def update_sector_graph(sector):
    dff = df_sectors.copy()
    dff = dff[#(dff['Sector']=='Index') | 
    (dff['Sector'].isin(sector))]
    return sectors_line(dff)

@callback(
    Output(component_id = 'stock-graph', component_property = 'figure'),
    Input(component_id = 'stocks-dropdown', component_property = 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
        )

def update_stock_graph(stock, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    #print(type(start_date))
    dff = df_stocks.copy()
    dff = dff[(dff['Name'].isin(stock)) & (dff['Date']>start_date) & (dff['Date']< end_date)]
    #dff = dff.loc[start_date:end_date]
    return stocks_line(dff)