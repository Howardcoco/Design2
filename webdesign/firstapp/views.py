from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
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
table = dynamodb.Table('designDB2')

response = table.scan(
    FilterExpression=Attr('sensor_message').eq('water')
)

items = response['Items']


decimal = []
time = []

def getdecimal():
    for i in range(len(items)):
        record = []
        record = items[i]['sensor_data']['sensor_data']
        decimal.append(record)
    #print(decimal)
    return decimal

def gettime():
    for i in range(len(items)):
        record = []
        record = items[i]['sensor_data']['time']
        time.append(record)
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










