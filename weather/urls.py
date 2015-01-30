__author__ = 'tneier'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('weather.views',
    ('daily/$', 'daily'),
    ('daily/(?P<days>\d+)$', 'dailynum'),
    ('sun/$', 'sun'),
    ('sun/(?P<days>\d+)$', 'sundays'),
)