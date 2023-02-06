from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout =  html.Div(children=[
        dbc.Row([
            dbc.Col(children = [
            dbc.Row([
                html.Img(
                    src = 'https://raw.githubusercontent.com/anacmqui/Checkpoint5/main/wine.png',#style= {'width':'auto'}
                ),
            ], style= {'width':'100%'}
            ),
            html.Hr(),
            html.P("Discover:", className="lead",
                    style={"top": 0,
                            "left": 0,
                            "bottom": 0,
                            "width": "25rem",
                            "padding": "2rem 1rem",
                            'font-size': '1rem',
                            'font-weight': 'bold'}
                ),
            html.Div([html.Div(
                dcc.Link(
                    f"{page['name']}",# - {page['path']}", 
                    href=page["relative_path"],
                    style={"top": 0,
                                "left": 0,
                                "bottom": 0,
                                "width": "25rem",
                                "padding": "2rem 1rem",
                                'font-size': '1.2rem',
                                'font-family': 'sans-serif',
                                'line-height': '2.5rem',
                                'color':'#4A4A4A'}
                )
            )
            for page in dash.page_registry.values()
                    ]
                ),], width= 2, style = {"background-color": "#607B8B", 'height':'1000000px'}, align='stretch'
            ),
            dbc.Col(children = [dash.page_container], width= 10)])
])

if __name__ == '__main__':
	app.run_server(debug=True)