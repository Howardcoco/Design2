from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
import boto3

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
    dynamo_response = get_dynamo_data()
    items = dynamo_response['Items']
    data = parse_data(items)
    print(item)

def index(request):
    context=item
    print(item)
    return HttpResponse(format(context))

def get_dynamo_data():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('designDB2')
    pe = 'time, sensor_message'
    response = table.scan(
        ProjectionExpression=pe,
        )
    while 'sensor_message' in response:
        response = table.scan(
            ProjectionExpression=pe,
            ExclusiveStartKey=response['sensor_message']
            )
    return response

# def search(request):
#     # template = loader.get_template('firstapp/search.html')
#     context = {}
#     return render(request, 'firstapp/templetes/firstapp/search.html', context)

