from django.conf.urls import patterns, include, url
from progress_crm_reporting.views import SQLQueryView, SQLResultView

urlpatterns = patterns('',
    url(r'^sql_query/', SQLQueryView.as_view(), name="sql_query_form"),
    url(r'^sql_result/', SQLResultView.as_view(), name="sql_query_result"),
)