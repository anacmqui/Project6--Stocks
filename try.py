from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

## WHAT YOU DISPLAY
# Additional Variables
# Style Pars


# Data
airbnb = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/airbnb_lisbon_1480_2017-07-27.csv')
airbnb_rev_by_neigh = airbnb.groupby('neighborhood')['reviews'].sum().reset_index()

# Display Details
par = 'Dash: A web application framework for your data.'
# fig_n_review_count = px.bar(airbnb_rev_by_neigh, x = "neighborhood", y = "reviews")
# dropdown_fig_list = list(map(lambda bed: str(int(bed)),airbnb['bedrooms'].unique())) + ['All']
dropdown_fig_dbc = list(map(lambda bed: dbc.DropdownMenuItem(str(int(bed))),airbnb['bedrooms'].unique())) #+ [dbc.DropdownMenuItem('All')]


# Additional Functions
def fig_n_review_count(df = airbnb_rev_by_neigh):
    return px.bar(df, x = "neighborhood", y = "reviews")

# WHERE YOU DISPLAY
# Layout
app.layout = html.Div(children=[
        dbc.Row(children = [
            html.H1(
                children = ['Hello Dash'],
                # className = '--bs-danger-text'
                ),
            html.H2(
                children = ['Whatever'],
                style = {'color': 'blue'}, 
            ),
        ], style = {'margin': '20px'},
        ),

        dbc.Row([
            html.P([par])
        ]),

        dbc.Row([
            dbc.Col([       
                # dcc.Dropdown(options = dropdown_fig_list, value = '1', id = 'bedrooms-dropdown', placeholder = 'Select a n of bedrooms'),   
                # dbc.Select(
                #     label="n Bedorooms",
                #     children = dropdown_fig_dbc,
                #     id = 'bedrooms-dropdown',
                # ),
                dbc.Select(
                    options=[
                        {"label": "Studio", "value": 0},
                        {"label": "All options", "value": 'All'},
                        {"label": "1 Bedroom", "value": 1},
                    ],
                    id="bedrooms-radio",
                ),
                # dbc.RadioItems(
                #     options=[
                #         {"label": "Studio", "value": 0},
                #         {"label": "All options", "value": 'All'},
                #         {"label": "1 Bedroom", "value": 1},
                #     ],
                #     value = 1,
                #     id="bedrooms-radio",
                # ),
            ]),

            dbc.Col(
                dcc.Graph(
                    id='fig-n-review-count-graph',
                    figure = fig_n_review_count()
                ),   
            width = 10,
            ),
        ]),
    ])



# HOW THEY CHANGE
# Callbacks
@app.callback(
    Output(component_id = 'fig-n-review-count-graph', component_property = 'figure'),
    # Input(component_id = 'bedrooms-dropdown', component_property = 'value'),
    Input(component_id = 'bedrooms-radio', component_property = 'value'),
)
def callback_function_name(beds):
    if beds == 'All' or beds is None:
    # print(beds)
    # if beds == 'All':
        airbnb_by_bedroom =airbnb.groupby('neighborhood')['reviews'].sum().reset_index()
    else:
        print(beds)
        beds = float(beds)
        airbnb_by_bedroom = airbnb[airbnb['bedrooms'] == beds].groupby('neighborhood')['reviews'].sum().reset_index()
    return fig_n_review_count(airbnb_by_bedroom)
 

# Call to run the App
if __name__ == '__main__':
    app.run_server(debug = True)