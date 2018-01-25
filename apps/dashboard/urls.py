from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.BaseURL.as_view(), name='baseurl'),
  url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
]

