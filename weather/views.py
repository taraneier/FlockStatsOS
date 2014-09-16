__author__ = 'tneier'
from models import Dailysummary
import json
from django.http import HttpResponse
from django.db import connection


def daily(request):
    dailynum(request, 180)


def dailynum(request, days):
    cursor = connection.cursor()
    query = "select unix_timestamp(date), cast(meantempi as Signed), cast(maxtempi as signed), cast(mintempi as signed), cast(precipi as signed) from weather.dailysummary limit " + days + ";"
    response_data = []

    avgval = []
    maxval = []
    minval = []
    precip = []
    cursor.execute(query)
    for row in cursor.fetchall():
        avgval.append([row[0]*1000, row[1]])
        maxval.append([row[0]*1000, row[2]])
        minval.append([row[0]*1000, row[3]])
        precip.append([row[0]*1000, row[4]])
    mintemp = {"key": "Low",
               "values": minval}
    maxtemp = {"key": "High",
               "values": maxval}
    avgtemp = {"key": "Avg",
               "values": avgval}
    precip = {"key": "Rain",
              "values": precip}

    response_data.append(mintemp)
    response_data.append(maxtemp)
    response_data.append(avgtemp)
    response_data.append(precip)

    return HttpResponse(json.dumps(response_data), content_type="application/json")