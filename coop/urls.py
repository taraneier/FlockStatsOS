__author__ = 'tneier'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('coop.views',
                       ('upload$', 'upload'),
                       ('upload/(?P<hum>\d+\.\d+)/(?P<t0>\d+\.\d+)/(?P<t1>\d+\.\d+)/(?P<t2>\d+\.\d+)/(?P<t3>\d+\.\d+)/(?P<t4>\d+\.\d+)/(?P<t5>\d+\.\d+)/(?P<t6>\d+\.\d+)/(?P<lum1>\d+)/(?P<lum2>\d+)/(?P<door>\d+)$',
                           'upload'),
                       # ('eggsbysite$', 'eggsbysite'),
                       # ('gramsbybird$', 'gramsbybird'),
                       # ('detail$', 'detail'),
                       # ('overview$', 'overview'),
                       # ('crosstab$', 'crosstab')
)