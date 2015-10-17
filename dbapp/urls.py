from django.conf.urls import patterns, url
from .views import dbaction_ajax, modal_detail, excel_output, dbselect_ajax, db_tables_ajax, appaction_ajax, modal_sql_script
urlpatterns = patterns('',

    url(r'^modal_detail/(?P<id>\d+)/$', modal_detail, name='modal_detail'),
#    url(r'^dbaction/$', dbaction, name='dbaction'),
    url(r'^dbaction_excel_output/$', excel_output, name='excel'),
    url(r'^dbaction_ajax/(?P<id>\d+)/(?P<execute_status>\d+)/$', dbaction_ajax, name='dbaction_ajax'),
    url(r'^dbselect_ajax/$', dbselect_ajax),
    url(r'^db_tables_ajax/$', db_tables_ajax),
    url(r'^appaction_ajax/$', appaction_ajax, name="appaction_ajax"),
    url(r'^modal_sql_script/$', modal_sql_script, name="modal_sql_script"),
)

