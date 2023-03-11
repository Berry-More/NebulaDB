import dash
import dash_bootstrap_components as dbc
import os
import requests
import pandas as pd

from dash import dcc, html, Input, Output, dash_table
import dash_cytoscape as cyto


def dash_app(flask_app):

    app = dash.Dash(
        server=flask_app, name='DashBoard', url_base_pathname='/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    """ LAYOUT """
    app.layout = html.Div([
        dbc.Row(html.H1('Nebula DB server'), style={'margin-bottom': '20px',
                                                    'margin-top': '10px'}),

        dbc.Row([
                dcc.Input(id='input-command', debounce=True,
                          type='text', placeholder='enter your command'),
                ], style={'margin-bottom': '30px', 'margin-top': '10px',
                          'width': '75%', 'margin-left': '5px'}),
        dbc.Row([
            html.Div('Current command:', style={'text-align': 'left', 'margin-top': '20px'}),
            html.Div(id='info-tab', style={'color': 'green', 'text-align': 'left',
                                           'margin-bottom': '30px'}),
            cyto.Cytoscape(
                id='cyto-figure',
                layout={'name': 'cose', 'padding': 50,
                        'componentSpacing': 200,
                        'nodeRepulsion': 10000,
                        'edgeElasticity': 100000},  # circle random cose
                maxZoom=1,
                minZoom=0.1,
                style={'width': '1500px', 'height': '600px'},
                elements=[]
            )
        ]),

        dbc.Row([
            html.Div('Data table:', style={'text-align': 'left', 'margin-top': '20px'}),
            dash_table.DataTable(id='data-tab', data=[],
                                 style_cell={'textAlign': 'center'},
                                 style_header={'backgroundColor': 'lavender'})
        ])

        ], style={'margin-left': '25px', 'margin-right': '25px'})

    @app.callback(
        [Output('info-tab', 'children'),
         Output('data-tab', 'data'),
         Output('data-tab', 'columns'),
         Output('cyto-figure', 'elements')],
        [Input('input-command', 'value')]
    )
    def enter_command(input_values):
        if type(input_values) == str:
            command = input_values
        else:
            command = 'none'

        path = os.path.join('http://127.0.0.1:5000/nebula/api/executes', command)
        response = requests.get(path).json()

        df = pd.DataFrame(response)
        df = df.applymap(str)

        cyto_data = []
        if len(df.columns) == 2:
            for i in range(len(df[df.columns[0]])):
                cyto_data.append({'data': {'id': df[df.columns[0]][i], 'label': df[df.columns[0]][i]}})
                cyto_data.append({'data': {'id': df[df.columns[1]][i], 'label': df[df.columns[1]][i]}})
                cyto_data.append({'data': {'source': df[df.columns[0]][i], 'target': df[df.columns[1]][i]}})
        else:
            cyto_data.append({'data': {'id': 'none', 'label': 'none'}})

        return command, df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], cyto_data

    return app
