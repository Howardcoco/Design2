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
import dash_daq as daq
from boto3.dynamodb.conditions import Key, Attr
from plotly.subplots import make_subplots

# get table from Dynamo
aws_access_key_id='AKIAZRDHJ7FL4THVQTF2'
aws_secret_access_key='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'
region='us-east-1'
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region
)
table = dynamodb.Table('FinalDesignDB')

# Scan the table
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


def getfirst(topic):
    response = table.scan(
        FilterExpression=Attr('topic').eq(topic)
    )
    items = response['Items']
    print(items)
    decimal = []
    time = []
    global timestamp
    timestamp=items[-1]['time']
    decimal.extend(getdecimal(items))
    time.extend(gettime(items))

    print(len(time))
    return items,decimal,time,timestamp

def getnext(X,Y,timestamp,topic):
        response2 = table.scan(
            FilterExpression=Attr('topic').eq(topic) & Attr('time').gt(timestamp)
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
        return X,Y,timestamp

#begin-plot-temperture
items1,decimal1,time1,timestamp1 = getfirst('building1/room00/water/lead')
items2,decimal2,time2,timestamp2 = getfirst('building1/room00/water/copper')
items3,decimal3,time3,timestamp3 = getfirst('building1/room00/water/turbidity')

X1=[]
Y1=[]
X1 = deque(maxlen=100)
Y1 = deque(maxlen=100)

X2=[]
Y2=[]
X2 = deque(maxlen=100)
Y2 = deque(maxlen=100)

X2=[]
Y2=[]
X3 = deque(maxlen=100)
Y3 = deque(maxlen=100)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.layout = html.Div(
    [
        html.Div(children=[
            html.Div(
                    daq.Gauge(
                        id='my-Gauge1',
                        label="lead",
                        color={"gradient":True,"ranges":{"green":[0,0.06],"yellow":[0.06,0.08],"red":[0.08,0.1]}},
                        value=0.02,
                        max=0.1,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge2',
                        label="copper",
                        color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                        value=2,
                        max=10,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge3',
                        label="turbidity",
                        color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                        value=2,
                        max=10,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'})
            ], style={'width': '100%', 'display': 'inline-block','margin-left': 200}),
        html.Div([
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=5*1000,
                n_intervals=0,
            ),], style={'margin-top': 0}),
    ]
)

@app.callback([Output('my-Gauge1', 'value'),
               Output('my-Gauge2', 'value'),
               Output('my-Gauge3', 'value'),
              #  Output('my-LED2', 'value'),
              # Output('my-LED-display-slider', 'value'),
              Output('live-graph', 'figure')],
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(n):


    global timestamp1
    global X1
    global Y1
    global start
    if n==0 and len(X1)==0:
        print("start")
        X1.extend(time1)
        Y1.extend(decimal1)
    else:
        # update the graph from specific timestamp
        X1,Y1,timestamp1=getnext(X1,Y1,timestamp1,'building1/room00/water/lead')

    global timestamp2
    global X2
    global Y2
    global start
    if n==0 and len(X2)==0:
        X2.extend(time2)
        Y2.extend(decimal2)
    else:
        # update the graph from specific timestamp
        X2,Y2,timestamp2=getnext(X2,Y2,timestamp2,'building1/room00/water/copper')

    global timestamp3
    global X3
    global Y3
    global start
    if n==0 and len(X3)==0:
        X3.extend(time3)
        Y3.extend(decimal3)
    else:
        # update the graph from specific timestamp
        X3,Y3,timestamp3=getnext(X3,Y3,timestamp3,'building1/room00/water/turbidity')

    # Generate subplot
    fig = make_subplots(
    rows=2, cols=2)

# go.Figure(data=go.Scatter(x=time, y=decimal))
    # fig = go.Figure(data=go.Scatter(x=X, y=Y))
    data1 = go.Scatter(
            x=list(X1),
            y=list(Y1),
            name='lead',
            mode= 'lines+markers',
            )
    data2 = go.Scatter(
            x=list(X2),
            y=list(Y2),
            name='copper',
            mode= 'lines+markers',
            )
    data3 = go.Scatter(
            x=list(X3),
            y=list(Y3),
            name='turbidity',
            mode= 'lines+markers',
            )
    #figure 1
    fig.add_trace(data1,row=1, col=1)
    fig.update_xaxes(range=[max(X1)-datetime.timedelta(days=1),max(X1)+datetime.timedelta(minutes=30)], row=1, col=1)
    fig.update_yaxes(range=[min(Y1),1.2*max(Y1)], row=1, col=1)
    fig.add_trace(data2,row=1, col=2)
    fig.update_xaxes(range=[max(X2)-datetime.timedelta(days=1),max(X2)+datetime.timedelta(minutes=30)], row=1, col=2)
    fig.update_yaxes(range=[min(Y2),1.2*max(Y2)], row=1, col=2)
    fig.add_trace(data3,row=2, col=1)
    fig.update_xaxes(range=[max(X3)-datetime.timedelta(days=1),max(X3)+datetime.timedelta(minutes=30)], row=2, col=1)
    fig.update_yaxes(range=[min(Y3),1.2*max(Y3)], row=2, col=1)

    #for all figures change the size of subplots
    fig.update_layout(height=600, width=1000)
    # figure = {'data': [data1],'layout' : go.Layout(xaxis=dict(range=[min(X1),max(X1)]),
    #                                             yaxis=dict(range=[min(Y1),max(Y1)]),)}
    value1=Y1[-1]
    value2=Y2[-1]
    value3=Y3[-1]
    return value1, value2, value3, fig


if __name__ == '__main__':
    app.run_server(debug=True)
