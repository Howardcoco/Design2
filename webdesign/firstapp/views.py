from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
import datetime
# import boto3
#
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('designDB2')
#
# response = table.get_item(
#    Key={
#         'time': '2019-9-4 8:28:35 PM',
#         'sensor_message': 'water'
#     }
# )
# item = response['Item']
# print(item)
# def index(request):
#     context=item
#     print(item)
#     return HttpResponse(format(context))

# def search(request):
#     # template = loader.get_template('firstapp/search.html')
#     context = {}
#     return render(request, 'firstapp/templetes/firstapp/search.html', context)
import boto3

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DATAfromSensor')

response = table.scan(
    FilterExpression=Attr('topic').eq('DesignPolicy/Room00/temperature')
)

items = response['Items']
print(items)
print('no')
decimal = []
time = []

def getdecimal():
    for i in range(len(items)):
        # record = []
        record = items[i]['payload_raw']
        # print(record.value.decode("utf-8"))
        a=record.value.decode("utf-8")
        a=float(a)
        a=round(a, 2)
        # print(type(a))
        decimal.append(a)
    #print(decimal)
    return decimal

def gettime():
    for i in range(len(items)):
        record = []
        record = items[i]['time']
        time.append(record)
    # print(time)
    return time

def gettime():
    for i in range(len(items)):
        timestamp = []
        timestamp = items[i]['time']
        inttime=[];
        record=[]
        # inttime= int(timestamp)
        # timeStamp = float(inttime/1000)
        # record = datetime.datetime.fromtimestamp(timeStamp)
        #print(record)
        time.append(timestamp)
        # print(timestamp)
        # print(record)
    #print(time)
    return time


getdecimal()
gettime()


# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
# import pylab as pl
plt.figure(figsize=(12, 5))
plt.plot(time, decimal, color='g', alpha=0.8)
plt.xlabel("Time")
plt.xticks(rotation = 90)
plt.ylabel("WaterQuality")
plt.title("Water Quality")
plt.show()
plt.savefig("examples.png")
# def index(request):
#     context=time
#     test=decimal
#     print(context)
#     return HttpResponse(format(test))

def index(request):
    # template = loader.get_template('firstapp/search.html')
    context = {}
    return render(request, 'firstapp/search.html', context)

