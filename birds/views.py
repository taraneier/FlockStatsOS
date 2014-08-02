from models import Bird, Breed, Flock
from rest_framework import viewsets
from django.db.models import Count
from birds.serializers import BirdSerializer, BreedSerializer, FlockSerializer

class FlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows birds to be viewed or edited.
    """
    queryset = Flock.objects.all()
    serializer_class = FlockSerializer


class BirdViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows birds to be viewed or edited.
    """
    queryset = Bird.objects.all()#.annotate(egg_count=Count('egg'))
    serializer_class = BirdSerializer


class BreedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows breeds to be viewed or edited.
    """
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer