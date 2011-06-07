from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('hack.vis.views',
    url(r'^$', 'main'),
    url(r'^data', 'data'),
    url(r'^info/(?P<id>.+)', 'info')
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
