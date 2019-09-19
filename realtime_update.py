import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import datetime
import boto3

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DATAfromSensor2')

response = table.scan(
    FilterExpression=Attr('topic').eq('DesignPolicy/Room00/temperature')
)
items = response['Items']
print(items)
decimal = []
time = []
global timestamp
timestamp=items[-1]['time']





def getdecimal(data_items):
    data_decimal=[]
    for i in range(len(data_items)):
        # record = []
        record = data_items[i]['payload_raw']
        # print(record.value.decode("utf-8"))
        a=record.value.decode("utf-8")
        a=float(a)
        a=round(a, 2)
        # print(type(a))
        data_decimal.append(a)
    #print(decimal)
    return data_decimal

def gettime(data_items):
    data_time=[];
    for i in range(len(data_items)):
        timestamp = data_items[i]['time']
        inttime= int(timestamp)
        timeStamp = float(inttime/1000)
        record = datetime.datetime.fromtimestamp(timeStamp)
        #print(record)
        data_time.append(record)
        # print(timestamp)
        # print(record)
    #print(time)
    return data_time

decimal.extend(getdecimal(items))
time.extend(gettime(items))

print(len(time))
print(time)

X=[]
Y=[]
X = deque(maxlen=100)
Y = deque(maxlen=100)
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div([
            html.H2('Room00',
                    style={
                        'color': 'darkblue',
                        'text-align':'center',
                    }),
        ]),
        html.Div([
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=5*1000,
                n_intervals=0,
            ),
        ]),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(n):

    print(n)
    global timestamp
    global X
    global Y
    global start
    if n==0 and len(X)==0:
        print("start")
        X.extend(time)
        Y.extend(decimal)
    else:
        #print(items2[len(items2)-1]['time'])
        response2 = table.scan(
            FilterExpression=Attr('topic').eq('DesignPolicy/Room00/temperature') & Attr('time').gt(timestamp)
        )
        items2 = response2['Items']

        if len(items2)!=0:
            print(len(items2))
            print(items2[len(items2)-1]['time'])
            print("test")
            decimal2=getdecimal(items2)
            time2=gettime(items2)
            print(decimal2)
            print(time2)
            # print(n)
            X.append(time2[0])     # Later this part will change into
            Y.append(decimal2[0])  #
            timestamp=items2[len(items2)-1]['time']


# go.Figure(data=go.Scatter(x=time, y=decimal))
    # fig = go.Figure(data=go.Scatter(x=X, y=Y))
    data = go.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    figure = {'data': [data],'layout' : go.Layout(title='Temperature',xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
