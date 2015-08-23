from django.contrib import admin
from django.conf.urls import patterns, include, url

from django_facebook_graph import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_facebook_graph.views.home', name='home'),
    # url(r'^django_facebook_graph/', include('django_facebook_graph.foo.urls')),

        # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^home/', views.add_product),
    url(r'^accounts/', include('allauth.urls')),
)
