from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auto_devops.views.home', name='home'),
    url(r'^', include('core.urls')),
    url(r'^', include('dbapp.urls')),
    url(r'^', include('sysapp.urls')),

#    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
