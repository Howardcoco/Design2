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




#extraction
items1,decimal1,time1,timestamp1 = getfirst('building1/room00/air/pm2.5')
items2,decimal2,time2,timestamp2 = getfirst('building1/room00/air/pm10')
items3,decimal3,time3,timestamp3 = getfirst('building1/room00/air/co2')
items4,decimal4,time4,timestamp4 = getfirst('building1/room00/air/co')
items5,decimal5,time5,timestamp5 = getfirst('building1/room00/air/o3')
items6,decimal6,time6,timestamp6 = getfirst('building1/room00/air/no2')
items7,decimal7,time7,timestamp7 = getfirst('building1/room00/air/tvoc')
items8,decimal8,time8,timestamp8 = getfirst('building1/room00/air/ch2o')


#inital-define
X1,X2,X3,X4,X5,X6,X7,X8 = [],[],[],[],[],[],[],[]
Y1,Y2,Y3,Y4,Y5,Y6,Y7,Y8 = [],[],[],[],[],[],[],[]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server
app.layout = html.Div(
    [
        html.Div(children=[
            html.Div(
                    daq.Gauge(
                        id='my-Gauge1',
                        label="PM2.5",
                        color={"gradient":True,"ranges":{"green":[0,9],"yellow":[9,15],"red":[15,20]}},
                        value=2,
                        max=20,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge2',
                        label="PM10",
                        color={"gradient":True,"ranges":{"green":[0,30],"yellow":[30,50],"red":[50,65]}},
                        value=10,
                        max=65,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge3',
                        label="CO2",
                        color={"gradient":True,"ranges":{"green":[0,480],"yellow":[480,800],"red":[800,1000]}},
                        value=100,
                        max=1000,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge4',
                        label="CO",
                        color={"gradient":True,"ranges":{"green":[0,5.4],"yellow":[5.4,9],"red":[9,12]}},
                        value=2,
                        max=12,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'})
            ], style={'width': '100%', 'display': 'inline-block','margin-left': 200}),


        html.Div(children=[
             html.Div(
                    daq.Gauge(
                        id='my-Gauge5',
                        label="NO2",
                        color={"gradient":True,"ranges":{"green":[0,30],"yellow":[30,51],"red":[51,70]}},
                        value=5,
                        max=70,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge6',
                        label="O3",
                        color={"gradient":True,"ranges":{"green":[0,30],"yellow":[30,53],"red":[53,70]}},
                        value=5,
                        max=70,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge7',
                        label="TVOC",
                        color={"gradient":True,"ranges":{"green":[0,300],"yellow":[300,500],"red":[500,700]}},
                        value=50,
                        max=700,
                        min=0,
                        size=150
                    ),style={'display': 'inline-block'}),
            html.Div(
                    daq.Gauge(
                        id='my-Gauge8',
                        label="CH20",
                        color={"gradient":True,"ranges":{"green":[0,16],"yellow":[16,27],"red":[27,35]}},
                        value=5,
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
               Output('my-Gauge5', 'value'),
               Output('my-Gauge6', 'value'),
               Output('my-Gauge7', 'value'),
               Output('my-Gauge8', 'value'),

              #  Output('my-LED2', 'value'),
              # Output('my-LED-display-slider', 'value'),
              Output('live-graph', 'figure')],
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(n):

    #PM2.5
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
        X1,Y1,timestamp1=getnext(X1,Y1,timestamp1,'building1/room00/air/pm2.5')

    #PM10
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
        X2,Y2,timestamp2=getnext(X2,Y2,timestamp2,'building1/room00/air/pm10')

    #CO2
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
        X3,Y3,timestamp3=getnext(X3,Y3,timestamp3,'building1/room00/air/co2')

    #CO
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
        X4,Y4,timestamp4=getnext(X4,Y4,timestamp4,'building1/room00/air/co')

    #o3
    global timestamp5
    global X5
    global Y5
    global start
    if n==0 and len(X5)==0:
        print("start5")
        X5.extend(time5)
        Y5.extend(decimal5)
    else:
        # update the graph from specific timestamp
        X5,Y5,timestamp5=getnext(X5,Y5,timestamp5,'building1/room00/air/o3')

    #NO2
    global timestamp6
    global X6
    global Y6
    global start
    if n==0 and len(X6)==0:
        print("start6")
        X6.extend(time6)
        Y6.extend(decimal6)
    else:
        # update the graph from specific timestamp
        X6,Y6,timestamp6=getnext(X6,Y6,timestamp6,'building1/room00/air/no2')

    #TVOC
    global timestamp7
    global X7
    global Y7
    global start
    if n==0 and len(X7)==0:
        print("start7")
        X7.extend(time7)
        Y7.extend(decimal7)
    else:
        # update the graph from specific timestamp
        X7,Y7,timestamp7=getnext(X7,Y7,timestamp7,'building1/room00/air/tvoc')

    #TVOC
    global timestamp8
    global X8
    global Y8
    global start
    if n==0 and len(X8)==0:
        print("start8")
        X8.extend(time8)
        Y8.extend(decimal8)
    else:
        # update the graph from specific timestamp
        X8,Y8,timestamp8=getnext(X8,Y8,timestamp8,'building1/room00/air/ch2o')

    # Generate subplot
    fig = make_subplots(
    rows=3, cols=3,subplot_titles=("PM2.5", "PM10", "CO2", "CO","O3","NO2","TVOC","CH2O"))

# go.Figure(data=go.Scatter(x=time, y=decimal))
    # fig = go.Figure(data=go.Scatter(x=X, y=Y))
    data1 = go.Scatter(
            x=list(X1),
            y=list(Y1),
            name='PM2.5',
            mode= 'lines+markers',
            )
    data2 = go.Scatter(
            x=list(X2),
            y=list(Y2),
            name='PM10',
            mode= 'lines+markers',
            )
    data3 = go.Scatter(
            x=list(X3),
            y=list(Y3),
            name='CO2',
            mode= 'lines+markers',
            )
    data4 = go.Scatter(
            x=list(X4),
            y=list(Y4),
            name='CO',
            mode= 'lines+markers',
            )
    data5 = go.Scatter(
            x=list(X5),
            y=list(Y5),
            name='O3',
            mode= 'lines+markers',
            )
    data6 = go.Scatter(
            x=list(X6),
            y=list(Y6),
            name='NO2',
            mode= 'lines+markers',
            )
    data7 = go.Scatter(
            x=list(X7),
            y=list(Y7),
            name='TVOC',
            mode= 'lines+markers',
            )
    data8 = go.Scatter(
            x=list(X8),
            y=list(Y8),
            name='CH2O',
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
    fig.add_trace(data3,row=1, col=3)
    # fig.update_xaxes(range=[max(X3)-datetime.timedelta(days=1),max(X3)+datetime.timedelta(minutes=30)], row=1, col=3)
    # fig.update_yaxes(range=[min(Y3),1.2*max(Y3)], row=2, col=1)
    #row2
    fig.add_trace(data4,row=2, col=1)
    # fig.update_xaxes(range=[max(X4)-datetime.timedelta(days=1),max(X4)+datetime.timedelta(minutes=30)], row=2, col=1)
    # fig.update_yaxes(range=[min(Y4),1.2*max(Y4)], row=1, col=1)
    fig.add_trace(data5,row=2, col=2)
    # fig.update_xaxes(range=[max(X5)-datetime.timedelta(days=1),max(X5)+datetime.timedelta(minutes=30)], row=2, col=2)
    # fig.update_yaxes(range=[min(Y5),1.2*max(Y5)], row=1, col=2)
    fig.add_trace(data6,row=2, col=3)
    # fig.update_xaxes(range=[max(X6)-datetime.timedelta(days=1),max(X6)+datetime.timedelta(minutes=30)], row=2, col=3)
    # fig.update_yaxes(range=[min(Y6),1.2*max(Y6)], row=2, col=1)
    #row3
    fig.add_trace(data7,row=3, col=1)
    # fig.update_xaxes(range=[max(X7)-datetime.timedelta(days=1),max(X7)+datetime.timedelta(minutes=30)], row=2, col=1)
    # fig.update_yaxes(range=[min(Y7),1.2*max(Y7)], row=1, col=1)
    fig.add_trace(data8,row=3, col=2)
    # fig.update_xaxes(range=[max(X8)-datetime.timedelta(days=1),max(X8)+datetime.timedelta(minutes=30)], row=2, col=2)
    # fig.update_yaxes(range=[min(Y8),1.2*max(Y8)], row=1, col=2)


    #for all figures change the size of subplots
    fig.update_layout(height=600, width=1000)
    # figure = {'data': [data1],'layout' : go.Layout(xaxis=dict(range=[min(X1),max(X1)]),
    #                                             yaxis=dict(range=[min(Y1),max(Y1)]),)}
    value1=Y1[-1]
    value2=Y2[-1]
    value3=Y3[-1]
    value4=Y4[-1]
    value5=Y5[-1]
    value6=Y6[-1]
    value7=Y7[-1]
    value8=Y8[-1]


    return value1, value2, value3, value4, value5, value6, value7, value8,fig


if __name__ == '__main__':
    app.run_server(debug=True)
