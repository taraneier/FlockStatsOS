from models import Bird, Breed, Flock
from rest_framework import viewsets
from django.shortcuts import render
from birds.serializers import BirdSerializer, BreedSerializer, FlockSerializer

def index(request):
    return render(request, 'index.html')


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
    queryset = Bird.objects.all()#.annotate(egg_count=Count('egg'))
    serializer_class = BirdSerializer


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer