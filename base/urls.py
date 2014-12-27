from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'babel.views.home', name='home'),
    # url(r'^create_account$', 'core.views.create_account', name='create_account'),

    url(r'^babel/', include('babel.urls')),

    url(r'^user_login/$', 'babel.views.user_login', name='user_login'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),

    # url(r'^handle_yoauth/', 'core.views.handle_yoauth', name='handle_yoauth'),
    url(r'^logout', 'babel.views.logout_view', name='logout'),

    url(r'^oauth/', 'babel.views.oauth', name='oauth'),

    url('', include('social.apps.django_app.urls', namespace='social')),
)
