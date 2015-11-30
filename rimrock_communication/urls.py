from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.JobListView.as_view(), name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^dispatched/$', views.action, name='dispatched'),
]