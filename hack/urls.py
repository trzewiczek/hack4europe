from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^start/', 'hack.vis.views.start'),
    url(r'^load/(?P<idef>[0-9]+)/', 'hack.vis.views.load' ),
)
