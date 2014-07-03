from django.conf.urls import patterns, include, url
from progress_crm.views import SQLView

urlpatterns = patterns('',
    url(r'^sql/', SQLView.as_view(), name="sql_url"),
)