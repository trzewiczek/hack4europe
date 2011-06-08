from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('hack.vis.views',
    url(r'^$', 'main'),
    url(r'^data/(?P<id>.+)', 'data'),
    url(r'^info/(?P<id>.+)', 'info'),
    url(r'^rights', 'rights')
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
