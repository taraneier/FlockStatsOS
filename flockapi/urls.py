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
    url(r'^crosstab.html', 'birds.views.crosstab', name='crosstab'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^weather/', include('weather.urls')),
    url(r'^stats/', include('stats.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
