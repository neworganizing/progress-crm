from django.conf.urls import patterns, include, url
from django.contrib import admin
from admin_tools.dashboard import registry as admin_tools_registry
from progress_crm.dashboard import CRMDashboard

admin.autodiscover()
admin_tools_registry.Registry.register(klass=CRMDashboard, app_name='progress_crm')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/progress_crm/reporting/', include('progress_crm_reporting.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
)