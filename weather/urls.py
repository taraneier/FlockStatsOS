__author__ = 'tneier'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('weather.views',
    ('daily/$', 'daily'),
    ('daily/(?P<days>\d{3})$', 'dailynum'),
    ('daily/(?P<days>\d{2})$', 'dailynum'),
    ('daily/(?P<days>\d{1})$', 'dailynum'),
)