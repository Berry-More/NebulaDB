import dash
import dash_bootstrap_components as dbc
import pandas as pd

from dash import dcc, html, Input, Output, dash_table
from functions import make_execute


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

""" TAB CONTENT """
tab1_content = dbc.Row([
    html.Div('Current command:', style={'text-align': 'left', 'margin-top': '20px'}),
    html.Div(id='info-tab', style={'color': 'green', 'text-align': 'left',
                                   'margin-bottom': '30px'}),
    dash_table.DataTable(id='data-tab', data=[])
    ])

""" LAYOUT """
app.layout = html.Div([
    dbc.Row(html.H1('Nebula DB server'), style={'margin-bottom': '20px',
                                                'margin-top': '10px'}),

    dbc.Row([
            dcc.Input(id='input-command', debounce=True,
                      type='text', placeholder='enter your command'),
            ], style={'margin-bottom': '30px', 'margin-top': '10px',
                      'width': '75%', 'margin-left': '5px'}),

    dbc.Tabs([
        dbc.Tab(tab1_content, label='Table'),
        dbc.Tab(html.Div('Place for another functions'), label='Visualisation')
    ])

    ], style={'margin-left': '25px', 'margin-right': '25px'})


@app.callback(
    [Output('info-tab', 'children'), Output('data-tab', 'data'),
     Output('data-tab', 'columns')],
    [Input('input-command', 'value')]
)
def enter_command(input_values):
    if type(input_values) == str:
        table_label = input_values
    else:
        table_label = 'none'
    execute = make_execute(input_values)
    df = pd.DataFrame(execute)
    df = df.applymap(str)
    return table_label, df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


if __name__ == '__main__':
    app.run_server(debug=True)
