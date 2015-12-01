from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.JobListView.as_view(), name='all_jobs'),
    url(r'^new/$', views.new, name='new'),
]