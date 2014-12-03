__author__ = 'tneier'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('stats.views',
    ('eggsbybird$', 'eggsbybird'),
    ('eggsbysite$', 'eggsbysite'),
    ('gramsbybird$', 'gramsbybird'),
    ('detail$', 'detail'),
    ('overview$', 'overview'),
    ('crosstab$', 'crosstab')
)