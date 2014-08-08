from models import Bird, Breed, Flock
from rest_framework import serializers

class FlockSerializer(serializers.HyperlinkedModelSerializer):
    bird_count = serializers.Field()
    egg_count = serializers.Field()
    avg_weight = serializers.Field()
    days_laying = serializers.Field()
    eggs_per_day = serializers.Field()
    favorite_sites = serializers.Field()
    top_layers = serializers.Field()
    last_week = serializers.Field()
    class Meta:
        model = Flock
        fields = ('flock_id','name','bird_count','egg_count','avg_weight','days_laying','eggs_per_day','favorite_sites', 'top_layers','last_week')


class BreedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Breed
        fields = ('breed_id','name', 'origin')

class BirdSerializer(serializers.HyperlinkedModelSerializer):
    age = serializers.Field()
    breed = serializers.HyperlinkedRelatedField
    egg_count = serializers.Field()
    avg_weight = serializers.Field()
    days_laying = serializers.Field()
    eggs_per_day = serializers.Field()
    favorite_site = serializers.Field()
    class Meta:
        model = Bird
        fields = ('bird_id','name', 'breed', 'hatched','age', 'egg_count', 'avg_weight', 'days_laying', 'eggs_per_day', 'favorite_site')
