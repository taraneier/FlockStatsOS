__author__ = 'tneier'
import json
from django.http import HttpResponse
from django.db import connection




def detail(request):
    cursor = connection.cursor()
    bird_query = "select bird_id, name from bird"
    response_data = []
    cursor.execute(bird_query)
    for bird in cursor.fetchall():
        query = "select unix_timestamp(date(`finish`)) as `x`,  CAST(sum(if(`e`.`bird_id` = %s, `weight`, 0)) as SIGNED) as `y` from `egg` `e` where finish > (curdate()-interval 2 week) group by `x` order by `x` desc;"
        cursor.execute(query, [bird[0]])
        values = []
        for row in cursor.fetchall():
            data = {"x": row[0]*1000, "y": row[1]}
            values.append(data)

        birddata = {"key": bird[1], "values": values}
        response_data.append(birddata)


    return HttpResponse(json.dumps(response_data), content_type="application/json")

def eggsbysite(request):
    cursor = connection.cursor()
    site_query = "select s.name as name, count(*) as count from site s join egg e on e.site_id = s.site_id group by name order by count desc limit 4;"
    response_data = []
    cursor.execute(site_query)
    for site in cursor.fetchall():
        data = {"label": site[0], "value": site[1]}
        response_data.append(data)

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def eggsbybird(request):
    cursor = connection.cursor()
    query = "select b.name as name, count(*) as count from bird b join egg e on e.bird_id = b.bird_id group by name order by count desc;"
    response_data = []
    cursor.execute(query)
    for site in cursor.fetchall():
        data = {"label": site[0], "value": site[1]}
        response_data.append(data)

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def overview(request):
    cursor = connection.cursor()
    query = "select unix_timestamp(date(finish)) as Date, count(*) as Qty, cast(sum(weight) as SIGNED) as Grams, avg(weight) as Average from egg where weight > 0 group by Date  order by Date desc limit 180;"
    response_data = []

    qtval = []
    wtval = []
    avgwt = []
    cursor.execute(query)
    for row in cursor.fetchall():
        qtval.append([row[0]*1000, row[1]])
        wtval.append([row[0]*1000, row[2]])
        avgwt.append([row[0]*1000, float(row[3])])

    qty = {"key": "Quantity",
           "bar": "true",
           "color": '#2ca02c',
           "values": qtval}
    weight = {"key": "Weight",
              "color": '#ff7f0e',
              "values": wtval}
    avgwgt = {"key": "Average",
              "color": "#0000ff",
              "values": avgwt}

    response_data.append(avgwgt)
    # response_data.append(weight)
    response_data.append(qty)


    return HttpResponse(json.dumps(response_data), content_type="application/json")
