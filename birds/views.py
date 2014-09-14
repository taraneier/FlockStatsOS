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


def overview(request):
    cursor = connection.cursor()
    bird_query = "select bird_id, name from bird"
    response_data = []
    cursor.execute(bird_query)
    for bird in cursor.fetchall():
        query = "select unix_timestamp(date(`finish`)) as `x`,  CAST(sum(if(`e`.`bird_id` = %s, `weight`, 0)) as SIGNED) as `y` from `egg` `e` where finish > (curdate()-interval 1 month) group by `x` order by `x` desc;"
        cursor.execute(query, [bird[0]])
        values = []
        for row in cursor.fetchall():
            data = {"x": row[0]*1000, "y": row[1]}
            values.append(data)

        birddata = {"key": bird[1], "values": values}
        response_data.append(birddata)


    return HttpResponse(json.dumps(response_data), content_type="application/json")