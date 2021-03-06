__author__ = 'tneier'
import json
from django.http import HttpResponse
from django.db import connection




def detail(request):
    cursor = connection.cursor()
    bird_query = "select bird_id, name from bird where active > 0"
    response_data = []
    cursor.execute(bird_query)
    for bird in cursor.fetchall():
        query = "select date(finish) as x, CAST(sum(if(`e`.`bird_id` = %s, `weight`, 0)) as SIGNED) as `y` from `egg` `e` where finish > (curdate()-interval 2 week) group by `x` order by `x` desc;"
        # query = "select date_format(date(finish), '%M %d, %Y') as Date, count(*) as Qty, cast(sum(weight) as SIGNED) as Grams, avg(weight) as Average, date(finish) as oDate from egg where weight > 0 group by Date  order by oDate desc limit 180;"

        cursor.execute(query, [bird[0]])

        values = []
        for row in cursor.fetchall():
            x = row[0].strftime("%B %d, %Y")
            data = {"x": x, "y": row[1]}
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


def gramsbybird(request):
    cursor = connection.cursor()
    query = "select b.name as name, cast(sum(weight) as UNSIGNED) as count from bird b join egg e on e.bird_id = b.bird_id group by name order by count desc;"
    response_data = []
    cursor.execute(query)
    for site in cursor.fetchall():
        data = {"label": site[0], "value": site[1]}
        response_data.append(data)

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def overview(request):
    cursor = connection.cursor()
    query = "select date_format(date(finish), '%M %d, %Y') as Date, count(*) as Qty, cast(sum(weight) as SIGNED) as Grams, avg(weight) as Average, date(finish) as oDate from egg where weight > 0 group by Date  order by oDate desc limit 90;"
    response_data = []

    qtval = []
    wtval = []
    avgwt = []
    cursor.execute(query)
    for row in cursor.fetchall():
        qtval.append([row[0], row[1]])
        wtval.append([row[0], row[2]])
        avgwt.append([row[0], float(row[3])])

    qty = {"key": "Quantity",
           "bar": "true",
           "color": '#5B90BF',
           "values": qtval}
    weight = {"key": "Weight",
              "color": '#ff7f0e',
              "values": wtval}
    avgwgt = {"key": "Average",
              "color": "#A2BF8A",
              "values": avgwt}

    response_data.append(avgwgt)
    # response_data.append(weight)
    response_data.append(qty)


    return HttpResponse(json.dumps(response_data), content_type="application/json")


def crosstab(request):
    cursor = connection.cursor()
    query = "select \
        date_format(date(finish), '%Y-%m-%d') as Date, \
        count(1) as `Total`, \
        cast(sum(if(`e`.`bird_id` = 8, `weight`, 0)) as SIGNED) as `Faith`,\
        cast(sum(if(`e`.`bird_id` = 1, `weight`, 0)) as SIGNED) as `Della`,\
        cast(sum(if(`e`.`bird_id` = 2, `weight`, 0)) as SIGNED) as `Ozzie`,\
        cast(sum(if(`e`.`bird_id` = 11, `weight`, 0)) as SIGNED) as `Ivy`,\
        cast(sum(if(`e`.`bird_id` = 7, `weight`, 0)) as SIGNED) as `Buffy`,\
        cast(sum(if(`e`.`bird_id` = 4, `weight`, 0)) as SIGNED) as `Barbara`,\
        cast(sum(if(`e`.`bird_id` = 9, `weight`, 0)) as SIGNED) as `Georgia`,\
        cast(sum(if(`e`.`bird_id` = 12, `weight`, 0)) as SIGNED) as `Winona`,\
        cast(sum(if(`e`.`bird_id` = 10, `weight`, 0)) as SIGNED) as `Mabel`,\
        cast(sum(if(`e`.`bird_id` = 3, `weight`, 0)) as SIGNED) as `Rosie`,\
        cast(sum(if(`e`.`bird_id` = 5, `weight`, 0)) as SIGNED) as `Sammy`,\
        cast(sum(if(`e`.`bird_id` = 6, `weight`, 0)) as SIGNED) as `Cappie`\
        from\
            `egg` `e`\
        group by `Date`\
        order by `Date` desc\
        ;"
    response_data = {}

    cursor.execute(query)
    # headings = []
    # for column in cursor.description:
        # headings.append(column[0])
    # response_data.append(headings)
    records = []
    columns = cursor.description
    for row in cursor.fetchall():
        response = {}
        # for i, column in cursor.description:
        for i in range(len(columns)):
            response[""+columns[i][0].lower()] = row[i]
        records.append(response)
        response_data = {'records': records}
    response_data['queryRecordCount'] = len(records)
    response_data['totalRecordCount'] = len(records)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
