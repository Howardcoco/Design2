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
def getdecimal(data_items): # get the values for a measurement
    data_decimal=[]
    for i in range(len(data_items)):
        # record = []
        record = data_items[i]['payload_raw'] #  get the payload
        # print(record.value.decode("utf-8"))
        a=record.value.decode("utf-8") # convert binary data
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
    response = table.scan( # search for the specific topic
        FilterExpression=Attr('topic').eq(topic)
    )
    items = response['Items']
    print(items)
    decimal = []
    time = []
    global timestamp
    timestamp=items[-1]['time']
    decimal.extend(getdecimal(items)) # store the data in decimal
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




#extraction
items1,decimal1,time1,timestamp1 = getfirst('building1/room00/thermal/db_temperature')
items2,decimal2,time2,timestamp2 = getfirst('building1/room00/thermal/humidity')
items3,decimal3,time3,timestamp3 = getfirst('building1/room00/thermal/air_speed')
items4,decimal4,time4,timestamp4 = getfirst('building1/room00/thermal/mr_temperature')



#inital-define
X1,X2,X3,X4 = [],[],[],[]
Y1,Y2,Y3,Y4 = [],[],[],[]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.layout = html.Div(
    [
        html.Div(children=[
            html.Div(
                    daq.Gauge(
                        id='my-Gauge1',
                        label="Dry-bulb temperature",
                        color={"gradient":True,"ranges":{"green":[0,15],"yellow":[15,30],"red":[30,45]}},
                        value=2,
                        max=45,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge2',
                        label="Relative humidity",
                        color={"gradient":True,"ranges":{"green":[0,0.6],"yellow":[0.6,1],"red":[1,1.3]}},
                        value=0.2,
                        max=1.3,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge3',
                        label="Air speed",
                        color={"gradient":True,"ranges":{"green":[0,0.6],"yellow":[0.6,1],"red":[1,1.3]}},
                        value=0.2,
                        max=1.3,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge4',
                        label="Mean radiant temperature",
                        color={"gradient":True,"ranges":{"green":[0,15],"yellow":[15,30],"red":[30,35]}},
                        value=2,
                        max=35,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'})
            ], style={'width': '100%', 'display': 'inline-block','margin-left': 200}),

        html.Div([
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=20000,
                n_intervals=0,
            ),], style={'margin-top': -10}),
    ]
)



@app.callback([Output('my-Gauge1', 'value'),
               Output('my-Gauge2', 'value'),
               Output('my-Gauge3', 'value'),
               Output('my-Gauge4', 'value'),

              #  Output('my-LED2', 'value'),
              # Output('my-LED-display-slider', 'value'),
              Output('live-graph', 'figure')],
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(n):

    #de-tem
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
        X1,Y1,timestamp1=getnext(X1,Y1,timestamp1,'building1/room00/thermal/db_temperature')

    #hum
    global timestamp2
    global X2
    global Y2
    global start
    if n==0 and len(X2)==0:
        print("start2")
        X2.extend(time2)
        Y2.extend(decimal2)
    else:
        # update the graph from specific timestamp
        X2,Y2,timestamp2=getnext(X2,Y2,timestamp2,'building1/room00/thermal/humidity')

    #air-speed
    global timestamp3
    global X3
    global Y3
    global start
    if n==0 and len(X3)==0:
        print("start3")
        X3.extend(time3)
        Y3.extend(decimal3)
    else:
        # update the graph from specific timestamp
        X3,Y3,timestamp3=getnext(X3,Y3,timestamp3,'building1/room00/thermal/air_speed')

    #mr-tem
    global timestamp4
    global X4
    global Y4
    global start
    if n==0 and len(X4)==0:
        print("start4")
        X4.extend(time4)
        Y4.extend(decimal4)
    else:
        # update the graph from specific timestamp
        X4,Y4,timestamp4=getnext(X4,Y4,timestamp4,'building1/room00/thermal/mr_temperature')


    # Generate subplot
    fig = make_subplots(
    rows=2, cols=2,subplot_titles=("Dry-bulb temperature", "Relative humidity", "Air speed", "Mean radiant temperature"))

# go.Figure(data=go.Scatter(x=time, y=decimal))
    # fig = go.Figure(data=go.Scatter(x=X, y=Y))
    data1 = go.Scatter(
            x=list(X1),
            y=list(Y1),
            name='Dry-bulb temperature',
            mode= 'lines+markers',
            )
    data2 = go.Scatter(
            x=list(X2),
            y=list(Y2),
            name='Relative humidity',
            mode= 'lines+markers',
            )
    data3 = go.Scatter(
            x=list(X3),
            y=list(Y3),
            name='Air speed',
            mode= 'lines+markers',
            )
    data4 = go.Scatter(
            x=list(X4),
            y=list(Y4),
            name='Mean radiant temperature',
            mode= 'lines+markers',
            )

    #plot
    #row1
    fig.add_trace(data1,row=1, col=1)
    # fig.update_xaxes(range=[max(X1)-datetime.timedelta(days=1),max(X1)+datetime.timedelta(minutes=30)], row=1, col=1)
    # fig.update_yaxes(range=[min(Y1),1.2*max(Y1)], row=1, col=1)
    fig.add_trace(data2,row=1, col=2)
    # fig.update_xaxes(range=[max(X2)-datetime.timedelta(days=1),max(X2)+datetime.timedelta(minutes=30)], row=1, col=2)
    # fig.update_yaxes(range=[min(Y2),1.2*max(Y2)], row=1, col=2)
    #fig.add_trace(data3,row=1, col=3)
    # fig.update_xaxes(range=[max(X3)-datetime.timedelta(days=1),max(X3)+datetime.timedelta(minutes=30)], row=1, col=3)
    # fig.update_yaxes(range=[min(Y3),1.2*max(Y3)], row=2, col=1)
    #row2
    fig.add_trace(data3,row=2, col=1)
    # fig.update_xaxes(range=[max(X4)-datetime.timedelta(days=1),max(X4)+datetime.timedelta(minutes=30)], row=2, col=1)
    # fig.update_yaxes(range=[min(Y4),1.2*max(Y4)], row=1, col=1)
    fig.add_trace(data4,row=2, col=2)
    # fig.update_xaxes(range=[max(X5)-datetime.timedelta(days=1),max(X5)+datetime.timedelta(minutes=30)], row=2, col=2)
    # fig.update_yaxes(range=[min(Y5),1.2*max(Y5)], row=1, col=2)
    #fig.add_trace(data6,row=2, col=3)
    # fig.update_xaxes(range=[max(X6)-datetime.timedelta(days=1),max(X6)+datetime.timedelta(minutes=30)], row=2, col=3)
    # fig.update_yaxes(range=[min(Y6),1.2*max(Y6)], row=2, col=1)
    #row3
    #fig.add_trace(data7,row=3, col=1)
    # fig.update_xaxes(range=[max(X7)-datetime.timedelta(days=1),max(X7)+datetime.timedelta(minutes=30)], row=2, col=1)
    # fig.update_yaxes(range=[min(Y7),1.2*max(Y7)], row=1, col=1)
    #fig.add_trace(data8,row=3, col=2)
    # fig.update_xaxes(range=[max(X8)-datetime.timedelta(days=1),max(X8)+datetime.timedelta(minutes=30)], row=2, col=2)
    # fig.update_yaxes(range=[min(Y8),1.2*max(Y8)], row=1, col=2)


    #for all figures change the size of subplots
    fig.update_layout(height=600, width=1200)
    # figure = {'data': [data1],'layout' : go.Layout(xaxis=dict(range=[min(X1),max(X1)]),
    #                                             yaxis=dict(range=[min(Y1),max(Y1)]),)}
    value1=Y1[-1]
    value2=Y2[-1]
    value3=Y3[-1]
    value4=Y4[-1]


    return value1, value2, value3, value4,fig


if __name__ == '__main__':
    app.run_server(debug=True)

