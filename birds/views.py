from models import Bird, Breed, Flock
from rest_framework import viewsets
from django.shortcuts import render
from birds.serializers import BirdSerializer, BreedSerializer, FlockSerializer
import json
from django.http import HttpResponse
from django.db import connection


def index(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard.html')


class FlockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows flocks to be viewed.
    """
    queryset = Flock.objects.all()
    serializer_class = FlockSerializer


class BirdViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows birds to be viewed or edited.
    """
    queryset = Bird.objects.all()  # .annotate(egg_count=Count('egg'))
    serializer_class = BirdSerializer


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


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
    # total_query = "select count(*) from egg;"
    # cursor.execute(total_query)
    # row = cursor.fetchone()
    # if (row):
    #     total = row[0]

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

#
# def overview(request):
#     cursor = connection.cursor()
#     query = "select unix_timestamp(date(finish)) as Date, count(*) as Qty, cast(sum(weight) as SIGNED) as Grams, cast(avg(weight) as SIGNED) as Average from egg where weight > 0 group by Date  order by Date desc limit 7;"
#     response_data = []
#
#     qtval = []
#     wtval = []
#     avgwt = []
#     cursor.execute(query)
#     for row in cursor.fetchall():
#         qtval.append({"x": row[0]*1000, "y": row[1]})
#         wtval.append({"x": row[0]*1000, "y": row[2]})
#         avgwt.append({"x": row[0]*1000, "y": row[3]})
#
#     qty = {"key": "Quantity",
#            "color": '#2ca02c',
#            "values": qtval}
#     weight = {"key": "Weight",
#               "color": '#ff7f0e',
#               "values": wtval}
#     avgwgt = {"key": "Average",
#               "color": "#0000ff",
#               "values": avgwt}
#     response_data.append(qty)
#     response_data.append(weight)
#     response_data.append(avgwgt)
#
#     return HttpResponse(json.dumps(response_data), content_type="application/json")


def overview(request):
    cursor = connection.cursor()
    query = "select unix_timestamp(date(finish)) as Date, count(*) as Qty, cast(sum(weight) as SIGNED) as Grams, cast(avg(weight) as SIGNED) as Average from egg where weight > 0 group by Date  order by Date desc;"
    response_data = []

    qtval = []
    wtval = []
    avgwt = []
    cursor.execute(query)
    for row in cursor.fetchall():
        qtval.append([row[0]*1000, row[1]])
        wtval.append([row[0]*1000, row[2]])
        avgwt.append([row[0]*1000, row[3]])

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

    response_data.append(weight)
    response_data.append(qty)
    response_data.append(avgwgt)

    return HttpResponse(json.dumps(response_data), content_type="application/json")




# [
#   {
#     "key" : "Quantity",
#     "bar": true,
#     "values" : [ [ 1136005200000 , 1271000.0] , [ 1138683600000 , 1271000.0] , [ 1141102800000 , 1271000.0] , [ 1143781200000 , 0] , [ 1146369600000 , 0] , [ 1149048000000 , 0] , [ 1151640000000 , 0] , [ 1154318400000 , 0] , [ 1156996800000 , 0] , [ 1159588800000 , 3899486.0] , [ 1162270800000 , 3899486.0] , [ 1164862800000 , 3899486.0] , [ 1167541200000 , 3564700.0] , [ 1170219600000 , 3564700.0] , [ 1172638800000 , 3564700.0] , [ 1175313600000 , 2648493.0] , [ 1177905600000 , 2648493.0] , [ 1180584000000 , 2648493.0] , [ 1183176000000 , 2522993.0] , [ 1185854400000 , 2522993.0] , [ 1188532800000 , 2522993.0] , [ 1191124800000 , 2906501.0] , [ 1193803200000 , 2906501.0] , [ 1196398800000 , 2906501.0] , [ 1199077200000 , 2206761.0] , [ 1201755600000 , 2206761.0] , [ 1204261200000 , 2206761.0] , [ 1206936000000 , 2287726.0] , [ 1209528000000 , 2287726.0] , [ 1212206400000 , 2287726.0] , [ 1214798400000 , 2732646.0] , [ 1217476800000 , 2732646.0] , [ 1220155200000 , 2732646.0] , [ 1222747200000 , 2599196.0] , [ 1225425600000 , 2599196.0] , [ 1228021200000 , 2599196.0] , [ 1230699600000 , 1924387.0] , [ 1233378000000 , 1924387.0] , [ 1235797200000 , 1924387.0] , [ 1238472000000 , 1756311.0] , [ 1241064000000 , 1756311.0] , [ 1243742400000 , 1756311.0] , [ 1246334400000 , 1743470.0] , [ 1249012800000 , 1743470.0] , [ 1251691200000 , 1743470.0] , [ 1254283200000 , 1519010.0] , [ 1256961600000 , 1519010.0] , [ 1259557200000 , 1519010.0] , [ 1262235600000 , 1591444.0] , [ 1264914000000 , 1591444.0] , [ 1267333200000 , 1591444.0] , [ 1270008000000 , 1543784.0] , [ 1272600000000 , 1543784.0] , [ 1275278400000 , 1543784.0] , [ 1277870400000 , 1309915.0] , [ 1280548800000 , 1309915.0] , [ 1283227200000 , 1309915.0] , [ 1285819200000 , 1331875.0] , [ 1288497600000 , 1331875.0] , [ 1291093200000 , 1331875.0] , [ 1293771600000 , 1331875.0] , [ 1296450000000 , 1154695.0] , [ 1298869200000 , 1154695.0] , [ 1301544000000 , 1194025.0] , [ 1304136000000 , 1194025.0] , [ 1306814400000 , 1194025.0] , [ 1309406400000 , 1194025.0] , [ 1312084800000 , 1194025.0] , [ 1314763200000 , 1244525.0] , [ 1317355200000 , 475000.0] , [ 1320033600000 , 475000.0] , [ 1322629200000 , 475000.0] , [ 1325307600000 , 690033.0] , [ 1327986000000 , 690033.0] , [ 1330491600000 , 690033.0] , [ 1333166400000 , 514733.0] , [ 1335758400000 , 514733.0]]
#   },
#   {
#     "key" : "Price",
#     "values" : [ [ 1136005200000 , 71.89] , [ 1138683600000 , 75.51] , [ 1141102800000 , 68.49] , [ 1143781200000 , 62.72] , [ 1146369600000 , 70.39] , [ 1149048000000 , 59.77] , [ 1151640000000 , 57.27] , [ 1154318400000 , 67.96] , [ 1156996800000 , 67.85] , [ 1159588800000 , 76.98] , [ 1162270800000 , 81.08] , [ 1164862800000 , 91.66] , [ 1167541200000 , 84.84] , [ 1170219600000 , 85.73] , [ 1172638800000 , 84.61] , [ 1175313600000 , 92.91] , [ 1177905600000 , 99.8] , [ 1180584000000 , 121.191] , [ 1183176000000 , 122.04] , [ 1185854400000 , 131.76] , [ 1188532800000 , 138.48] , [ 1191124800000 , 153.47] , [ 1193803200000 , 189.95] , [ 1196398800000 , 182.22] , [ 1199077200000 , 198.08] , [ 1201755600000 , 135.36] , [ 1204261200000 , 125.02] , [ 1206936000000 , 143.5] , [ 1209528000000 , 173.95] , [ 1212206400000 , 188.75] , [ 1214798400000 , 167.44] , [ 1217476800000 , 158.95] , [ 1220155200000 , 169.53] , [ 1222747200000 , 113.66] , [ 1225425600000 , 107.59] , [ 1228021200000 , 92.67] , [ 1230699600000 , 85.35] , [ 1233378000000 , 90.13] , [ 1235797200000 , 89.31] , [ 1238472000000 , 105.12] , [ 1241064000000 , 125.83] , [ 1243742400000 , 135.81] , [ 1246334400000 , 142.43] , [ 1249012800000 , 163.39] , [ 1251691200000 , 168.21] , [ 1254283200000 , 185.35] , [ 1256961600000 , 188.5] , [ 1259557200000 , 199.91] , [ 1262235600000 , 210.732] , [ 1264914000000 , 192.063] , [ 1267333200000 , 204.62] , [ 1270008000000 , 235.0] , [ 1272600000000 , 261.09] , [ 1275278400000 , 256.88] , [ 1277870400000 , 251.53] , [ 1280548800000 , 257.25] , [ 1283227200000 , 243.1] , [ 1285819200000 , 283.75] , [ 1288497600000 , 300.98] , [ 1291093200000 , 311.15] , [ 1293771600000 , 322.56] , [ 1296450000000 , 339.32] , [ 1298869200000 , 353.21] , [ 1301544000000 , 348.5075] , [ 1304136000000 , 350.13] , [ 1306814400000 , 347.83] , [ 1309406400000 , 335.67] , [ 1312084800000 , 390.48] , [ 1314763200000 , 384.83] , [ 1317355200000 , 381.32] , [ 1320033600000 , 404.78] , [ 1322629200000 , 382.2] , [ 1325307600000 , 405.0] , [ 1327986000000 , 456.48] , [ 1330491600000 , 542.44] , [ 1333166400000 , 599.55] , [ 1335758400000 , 583.98]]
#   }
# ]

