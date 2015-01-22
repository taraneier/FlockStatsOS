__author__ = 'tneier'
import json
from django.http import HttpResponse
from django.db import connection


def upload(request, hum, t0, t1, t2, t3, t4, t5, t6, lum1, lum2, door):
    cursor = connection.cursor()
    insert_query = "insert into weather.monitor values (null, now(), %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s)"
    params = hum, t0, t1, t2, t3, t4, t5, t6, lum1, lum2, door
    cursor.execute(insert_query, params)
    response_data = []
    response_data.append("{ok}")
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def door(request):
    response_data = "Open"
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def lum1(request):
    response_data = {"value": 978}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
