from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^updates/(?P<profile_id>\w{0,50})/(?P<page>\d+)/$', 'babel.views.updates', name='babel_updates'),
    url(r'^new_update/(?P<update_id>\w{0,50})/$', 'babel.views.new_update', name='babel_new_update')
)