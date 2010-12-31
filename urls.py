from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^fwp/', include('fwp.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # This needs to come before the dynamic package URLs or it will be considered a package.
    (r'^testing/$','packageserver.views.testing'),

    (r'^$','packageserver.views.index'),
    (r'^(?P<package_name>[\w\-]+)/$','packageserver.views.package'),
    (r'^(?P<package_name>[\w\-]+)/(?P<package_version>[\d\.]+)/$','packageserver.views.package'),

)
