__author__ = 'tneier'
import json
from django.http import HttpResponse
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder

import datetime


def upload(request, hum, t0, t1, t2, t3, t4, t5, t6, lum1, lum2, door):
    cursor = connection.cursor()
    insert_query = "insert into weather.monitor values (null, now(), %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s)"
    params = hum, t0, t1, t2, t3, t4, t5, t6, lum1, lum2, door
    cursor.execute(insert_query, params)
    data = {
        "hum": hum,
        "t0": t0,
        "t1": t1,
        "t2": t2 ,
        "t3": t3,
        "t4": t4,
        "t5": t5,
        "t6": t6,
        "lum": lum1,
        "lum2": lum2,
        "door": door
           }
    latest_query = "update weather.latest set data = %s"
    cursor.execute(latest_query, [json.dumps(data, cls=DjangoJSONEncoder)])

    return HttpResponse(json.dumps(data), content_type="application/json")


def door(request):
    response_data = "Open"
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def lum1(request):
    response_data = {"value": 978}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def alldata2(request):
    cursor = connection.cursor()
    query = "select *, date_format(date(date), '%M %d, %Y  %H %m %s') from weather.monitor"
    response_data = []

    humidity = []
    t0 = []
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    t5 = []
    t6 = []
    lum1 = []
    lum2 = []
    door = []
    cursor.execute(query)
    for row in cursor.fetchall():
        rowdate = row[13]
        # date = datetime.datetime(year=rowdate.year, month=rowdate.month, day=rowdate.day, hour=row[1].hour, minute=row[1].minute)

        # set = datetime.datetime(year=rowdate.year, month=rowdate.month, day=rowdate.day,  hour=row[2].hour, minute=row[2].minute)
        # diff = set - rise
        # hours = round(diff.seconds / 60.00 / 60.00, 2);
        humidity.append([rowdate, row[2]])
        # moonshine.append([row[0], round(row[4],2)])
        # sunrise.append(row[1].strftime('%H:%M'))
        # sunset.append(row[2].strftime('%H:%M'))
    hum = {"key": "Humidity",
               "bar" : "true",
               "values": humidity}

    response_data.append(hum)
    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")



def alldata(request):
    cursor = connection.cursor()
    query = "select data from weather.latest"
    cursor.execute(query)
    data = cursor.fetchall()[0][0]
    return HttpResponse(data, content_type="application/json")




def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]
