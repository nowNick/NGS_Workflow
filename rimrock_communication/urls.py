from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.JobListView.as_view(), name='all_jobs'),
    url(r'^new/$', views.new, name='new'),
    url(r'^proxy_check/$', views.setup_proxy, name='setup_proxy'),
    url(r'^refresh_jobs/$', views.refresh_jobs, name='refresh_jobs'),
    url(r'^first_run_config/$', views.first_run_configuration, name='configure_env'),
    url(r'^(?P<job_id>[0-9]+)/$', views.refresh_output, name='detail'),
]