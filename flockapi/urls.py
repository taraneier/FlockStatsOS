from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'birds', views.BirdViewSet)
router.register(r'breeds', views.BreedViewSet)
router.register(r'flocks', views.FlockViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flockapi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
