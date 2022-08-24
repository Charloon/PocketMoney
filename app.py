import copy
from dash.dependencies import Output, Input, State
import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_auth
import pandas as pd
import numpy as np
from SendGetDataFrameS3 import *
from PocketMoneyPasswords import PocketMoneyPasswords

# initialize variable
init_money = 10
# kids name
KidName1 = "Clarisse"
Kidname2 = "Edouard"
# initialize dataframe
# fetch dataframes from s3 bucket
df1 = fetchDataframeFromS3("df1.csv", "s3")  # for kid 1
df2 = fetchDataframeFromS3("df2.csv", "s3")  # for kid 2
df0 = fetchDataframeFromS3("df0.csv", "s3")  # for reset
# set dataframes in state storage
dcc.Store(data=df1.to_dict('records'), id="df1")
dcc.Store(data=df2.to_dict('records'), id="df2")
dcc.Store(data=df0.to_dict('records'), id="df0")

# Define user password and login
# example for the login/password
# VALID_USERNAME_PASSWORD_PAIRS = ['login1', 'pwd1'], ['login2', "pwd2"]]
VALID_USERNAME_PASSWORD_PAIRS = PocketMoneyPasswords
# get list of possible tacks from dataframe
ActionList = df0["task"].values

## setup the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1, maximum-scale=1.8, minimum-scale=0.2'}])

# setup authentification, server and app title
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
app.title = "Pocket Money Cohens"

## drop downs
# drop down for kid 1
dropdown_1 = dcc.Dropdown(id="Action-1",
                          options=[
                              {"label": action, "value": action} for action in ActionList
                          ],
                          value="Dress the table",
                          clearable=False,
                          className="dropdown"
                          )

# drop down fo kid 2
dropdown_2 = dcc.Dropdown(id="Action-2",
                          options=[
                              {"label": action, "value": action}
                              for action in ActionList
                          ],
                          value="Dress the table",
                          clearable=False,
                          className="dropdown"
                          )

## tables
#for kid 1
table1 = dash_table.DataTable(
    id='data_table-1',
    style_data={
        'minWidth': '10px', 'width': '10px', 'maxWidth': '150px',
        'height': 'auto',
    },
    fill_width=True,
    data=df1.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df1.columns])
# for kid 2
table2 = dash_table.DataTable(
    id='data_table-2',
    style_data={
        'minWidth': '10px', 'width': '10px', 'maxWidth': '150px',
        'height': 'auto',
    },
    fill_width=True,
    data=df2.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df2.columns])

## define cards
# for kid 1
card_score1 = dbc.Card(
    dbc.CardBody(
        html.Div(
            children=[
                html.P(id='added value-1'),
                dcc.Store(data=df1.to_dict('records'), id="df1"),
                html.Div(
                    children=[
                        dbc.Row([
                            dbc.Col([
                                    dropdown_1
                                    ], width=10),
                            dbc.Col(
                                [html.Button('+', id='btn-nclicks-1-1', n_clicks=0)], width=2),
                        ]),
                        dbc.Row([
                            dbc.Col(
                                [html.P('Poket money for the month: ')], width="auto"),
                            dbc.Col([html.P(id="PoketMoney-1")], width="auto"),
                            dbc.Col([html.P(' euros')], width="auto")
                        ], no_gutters=False),
                        dbc.Row([
                            dbc.Col(
                                [table1])]),
                        dbc.Row([
                            dbc.Col(
                                [html.Button('Reset', id='btn-nclicks-2-1', n_clicks=0)])])
                    ]
                )
            ]
        )
    )
)

# for kid 2
card_score2 = dbc.Card(
    dbc.CardBody(
        html.Div(
            children=[
                html.P(id='added value-2'),
                dcc.Store(data=df2.to_dict('records'), id="df2"),
                html.Div(
                    children=[
                        dbc.Row([
                            dbc.Col([
                                    dropdown_2
                                    ], width=10),
                            dbc.Col(
                                [html.Button('+', id='btn-nclicks-1-2', n_clicks=0)], width=2),
                        ]),
                        dbc.Row([
                            dbc.Col(
                                [html.P('Poket money for the month: ')], width="auto"),
                            dbc.Col([html.P(id="PoketMoney-2")], width="auto"),
                            dbc.Col([html.P(' euros')], width="auto")
                        ], no_gutters=False),
                        dbc.Row([
                            dbc.Col(
                                [table2])]),
                        dbc.Row([
                            dbc.Col(
                                [html.Button('Reset', id='btn-nclicks-2-2', n_clicks=0)])])
                    ]
                )
            ]
        )
    )
)

# define tabs
tab1_content = [
    dbc.Row(
        [dbc.Col(card_score1),
         ],
    )]

tab2_content = [
    dbc.Row(
        [dbc.Col(card_score2),
         ],
    )]

tabs = dcc.Tabs(children=[
    dcc.Tab(tab1_content, label=KidName1),
    dcc.Tab(tab2_content, label=Kidname2),
], mobile_breakpoint=0)

# define app layout
app.layout = html.Div(tabs)

## callback for kid 1
# callback for checks to either add a task or reset the tables
@app.callback(
    [Output('added value-1', "children"),
     Output("df1", "data")],
    [Input('btn-nclicks-1-1', 'n_clicks'),
     Input('btn-nclicks-2-1', 'n_clicks'),
     State('Action-1', 'value'),
     State("df1", "data")]
)
def displayClick1(btn1, btn2, Action, data):
    df = pd.DataFrame(data)
    msg = ""
    trigger = dash.callback_context.triggered[0]

    if trigger["prop_id"] == 'btn-nclicks-1-1.n_clicks':
        df = fetchDataframeFromS3("df1.csv", "s3")
        df.loc[df["task"] == Action, "count"] += 1
        sendDataframeToS3(df, "df1.csv", "s3")
        dcc.Store(data=df.to_dict('records'), id="df1")
    elif trigger["prop_id"] == 'btn-nclicks-2-1.n_clicks':
        df = copy.deepcopy(df0)
        dcc.Store(data=df.to_dict('records'), id="df1")
        sendDataframeToS3(df, "df1.csv", "s3")

    df = fetchDataframeFromS3("df1.csv", "s3")
    dcc.Store(data=df.to_dict('records'), id="df1")
    return msg, df.to_dict('records')

# callback to update the calculation for kid 1
@app.callback(
    Output('PoketMoney-1', "children"),
    [Input('added value-1', 'children'),
     State("df1", "data")]
)
def updatePoketMoney1(addedValue, data):
    #msg = "Button 1 was most recently clicked"
    df = pd.DataFrame(data)
    return str(init_money + np.sum(df["count"].values*df["cost (eur)"].values))

# callback to update the dataframe
@app.callback(
    Output('data_table-1', "data"),
    [Input('added value-1', 'children'),
     State("df1", "data")]
)
def updateDataTable1(addedValue, data):
    df = pd.DataFrame(data)
    print("df1", df)
    return df.to_dict('records')

## callback for kid1
# callback for checks to either add a task or reset the tables
@app.callback(
    [Output('added value-2', "children"),
     Output("df2", "data")],
    [Input('btn-nclicks-1-2', 'n_clicks'),
     Input('btn-nclicks-2-2', 'n_clicks'),
     State('Action-2', 'value'),
     State("df2", "data")]
)
def displayClick2(btn1, btn2, Action, data):
    df = pd.DataFrame(data)
    msg = ""
    trigger = dash.callback_context.triggered[0]

    if trigger["prop_id"] == 'btn-nclicks-1-2.n_clicks':
        df = fetchDataframeFromS3("df2.csv", "s3")
        df.loc[df["task"] == Action, "count"] += 1
        sendDataframeToS3(df, "df2.csv", "s3")
    elif trigger["prop_id"] == 'btn-nclicks-2-2.n_clicks':
        df = copy.deepcopy(df0)
        sendDataframeToS3(df, "df2.csv", "s3")
    df = fetchDataframeFromS3("df2.csv", "s3")
    dcc.Store(data=df.to_dict('records'), id="df2")
    return msg, df.to_dict('records')

# callback to update the calculation for kid 2
@app.callback(
    Output('PoketMoney-2', "children"),
    [Input('added value-2', 'children'),
     State("df2", "data")]
)
def updatePoketMoney2(addedValue, data):
    df = pd.DataFrame(data)
    return str(init_money + np.sum(df["count"].values*df["cost (eur)"].values))

# callback to update the dataframe for kid 2
@app.callback(
    Output('data_table-2', "data"),
    Input('added value-2', 'children'),
    State("df2", "data")
)
def updateDataTable2(addedValue, data):
    df = pd.DataFrame(data)
    return df.to_dict('records')

# run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.3', port=8050)
