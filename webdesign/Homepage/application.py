import datetime
from collections import deque
import boto3
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from boto3.dynamodb.conditions import Attr
from dash.dependencies import Input, Output

aws_access_key_id = 'AKIAZRDHJ7FL4THVQTF2'
aws_secret_access_key = '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'
region = 'us-east-1'
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region
                          )
table = dynamodb.Table('FinalDesignDB')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.layout = html.Div(
    [
        html.Div([
            dcc.Interval(
                id='table-update',
                interval=10000,  # update interval
                n_intervals=0,
            ),
            dash_table.DataTable(
                id="live_table",
                columns=[
                    {"name": ["", "Room"], "id": "room"},
                    {"name": ["Air", "PM2.5"], "id": "pm2.5"},
                    {"name": ["Air", "PM10"], "id": "pm10"},
                    {"name": ["Air", "CO2"], "id": "co2"},
                    {"name": ["Air", "CO"], "id": "co"},
                    {"name": ["Air", "O3"], "id": "o3"},
                    {"name": ["Air", "NO2"], "id": "no2"},
                    {"name": ["Air", "TVOC"], "id": "tvoc"},
                    {"name": ["Air", "CH2O"], "id": "ch2o"},

                    {"name": ["Water", "Lead"], "id": "lead"},
                    {"name": ["Water", "Copper"], "id": "copper"},
                    {"name": ["Water", "Turbidity"], "id": "turbidity"},
                    {"name": ["Water", "Coilforms"], "id": "coilforms"},

                    {"name": ["Thermal", "Dry-bulb Temp"], "id": "db_temperature"},
                    {"name": ["Thermal", "Humidity"], "id": "humidity"},
                    {"name": ["Thermal", "Air Speed"], "id": "air_speed"},
                    {"name": ["Thermal", "Mean Radiant Temp"], "id": "mr_temperature"},
                ],
                data=[{
                    "room": "-",
                    "pm2.5": "-",
                    "pm10": "-",
                    "co2": "-",
                    "co": "-",
                    "o3": "-",
                    "no2": "-",
                    "tvoc": "-",
                    "ch2o": "-",
                    "lead": "-",
                    "copper": "-",
                    "turbidity": "-",
                    "coilforms": "-",
                    "db_temperature": "-",
                    "humidity": "-",
                    "air_speed": "-",
                    "mr_temperature": "-"
                }
                    for i in range(5)
                ],
                style_header={'backgroundColor': '#FFFFFF',
                              'color': 'black'},
                style_cell={
                    'backgroundColor': '#448ADF',
                    'color': 'white'
                },
                style_data_conditional=[
                    {
                        'if': {
                            'column_id': 'pm2.5',
                            'filter_query': '{pm2.5} > 15'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'pm10',
                            'filter_query': '{pm10} > 50'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'co2',
                            'filter_query': '{co2} > 800'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'co',
                            'filter_query': '{co} > 9'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'o3',
                            'filter_query': '{o3} > 51'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'no2',
                            'filter_query': '{no2} > 53'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'tvoc',
                            'filter_query': '{tvoc} > 500'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'ch2o',
                            'filter_query': '{ch2o} > 27'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'lead',
                            'filter_query': '{lead} > 0.01'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'copper',
                            'filter_query': '{copper} > 1.0'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'turbidity',
                            'filter_query': '{turbidity} > 1.0'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'coilforms',
                            'filter_query': '{coilforms} > 0'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'db_temperature',
                            'filter_query': '{db_temperature} > 30'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'humidity',
                            'filter_query': '{humidity} > 1'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'air_speed',
                            'filter_query': '{air_speed} > 1'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                    {
                        'if': {
                            'column_id': 'mr_temperature',
                            'filter_query': '{mr_temperature} > 30'
                        },
                        'backgroundColor': '#FF9E4E',
                        'color': 'white',
                    },
                ],
                merge_duplicate_headers=True
            )
        ])
    ]
)
type = ["/water/lead", "/water/copper", "/water/turbidity", "/water/coilforms",
        "/air/pm2.5", "/air/pm10", "/air/co2", "/air/co", "/air/o3", "/air/no2", "/air/tvoc", "/air/ch2o",
        "/thermal/db_temperature", "/thermal/humidity", "/thermal/air_speed", "/thermal/mr_temperature"]

# print(type[j].split("/")[-1])
global timestamps
timestamps=["0"]*25
global last_dash_table


@app.callback(Output('live_table', 'data'),
              [Input('table-update', 'n_intervals')])
def update_graph_scatter(n):
    global last_dash_table
    indicator=False
    df_empty = pd.DataFrame(columns=[
        "room",
        "lead",
        "copper",
        "turbidity",
        "coilforms",

        "pm2.5",
        "pm10",
        "co2",
        "co",
        "o3",
        "no2",
        "tvoc",
        "ch2o",

        "db_temperature",
        "humidity",
        "air_speed",
        "mr_temperature"
    ])
    for i in range(5):
        print(i)
        df_row = pd.DataFrame([{"room": "room" + str(i).zfill(2)}])
        topic = "building1/room" + str(i).zfill(2)
        print(topic)
        response = table.scan(
            FilterExpression=Attr('topic').begins_with(topic) #& Attr('time').gt(timestamps[i])
        )
        items = response['Items']
        print(items)
        if len(items) != 0:
            timestamps[i]=items[-1]['time']

        for j in range(len(type)):
            if len(items) == 0:
                value = "-"
            else:
                topic_actual="building1/room" + str(i).zfill(2) +type[j]
                for k in range(len(items)):
                    print(items[-1]['topic'])
                    if items[k]['topic']==topic_actual:
                        record = items[k]['payload_raw']
                        a=record.value.decode("utf-8")
                        a=float(a)
                        value=round(a, 2)
                        indicator=True
            # print(topic)
            # print(items1)
            id = type[j].split("/")[-1]
            df_value = pd.DataFrame([{id: value}])
            # print(df_value)
            df_row = df_row.join(df_value)
            # data=df.to_dict('records')
        #print(df_row)
        df_empty = df_empty.append(df_row)
    print(df_empty)
    if indicator==True:
        data=df_empty.to_dict('records')
        last_dash_table=data
    else:
        data=last_dash_table
    return data

if __name__ == '__main__':
    app.run_server(debug=True)
