from django.conf.urls import patterns, include, url
from rest_framework import routers
from birds import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from weather import urls

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'birds', views.BirdViewSet)
router.register(r'breeds', views.BreedViewSet)
router.register(r'flocks', views.FlockViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flockapi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^index.html', 'birds.views.index', name='index'),
    url(r'^dashboard.html', 'birds.views.dashboard', name='dashboard'),
    url(r'^stats/overview', 'birds.views.overview', name='overview'),
    url(r'^stats/bloverview', 'birds.views.bloverview', name='bloverview'),
    url(r'^stats/detail', 'birds.views.detail', name='detail'),
    url(r'^stats/eggsbysite', 'birds.views.eggsbysite', name='sites'),
    url(r'^stats/eggsbybird', 'birds.views.eggsbybird', name='birds'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^weather/', include('weather.urls')),
)
