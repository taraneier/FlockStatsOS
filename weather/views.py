__author__ = 'tneier'
import json
from django.http import HttpResponse
from django.db import connection
import datetime


def daily(request):
    return dailynum(request, "180")


def dailynum(request, days):
    cursor = connection.cursor()
    query = "select unix_timestamp(date), cast(meantempi as Signed), cast(maxtempi as signed), cast(mintempi as signed), cast(precipi as signed) from weather.dailysummary  order by date desc limit " + days + ";"
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
              "bar": "true",
              "values": precip}

    response_data.append(mintemp)
    response_data.append(maxtemp)
    response_data.append(avgtemp)
    response_data.append(precip)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def sun(request):
    return sundays(request, "180")


def sundays(request, days):
    cursor = connection.cursor()
    query = "select unix_timestamp(date), sunrise, sunset from weather.astro order by date desc limit " + days + ";"
    response_data = []

    sunrise = []
    sunset = []
    sunshine = []
    cursor.execute(query)
    for row in cursor.fetchall():
        rowdate = datetime.date.fromtimestamp(row[0])
        rise = datetime.datetime(year=rowdate.year, month=rowdate.month, day=rowdate.day, hour=row[1].hour, minute=row[1].minute)

        set = datetime.datetime(year=rowdate.year, month=rowdate.month, day=rowdate.day,  hour=row[2].hour, minute=row[2].minute)
        diff = set - rise
        hours = round(diff.seconds / 60.00 / 60.00, 2);
        sunshine.append([row[0]*1000, hours])
        sunrise.append(row[1].strftime('%H:%M'))
        sunset.append(row[2].strftime('%H:%M'))
    sun = {"key": "Hours of Daylight",
               "values": sunshine}
    rises = {"key": "Sunrise",
               "values": sunrise}
    sets = {"key": "Sunset",
               "values": sunset}

    response_data.append(sun)
    # response_data.append(rises)
    # response_data.append(sets)
    return HttpResponse(json.dumps(response_data), content_type="application/json")