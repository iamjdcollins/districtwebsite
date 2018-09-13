from django.conf.urls import url

from . import views

app_name = 'medialibrary'

urlpatterns = [
  url(r'^$', views.BaseURL.as_view(), name='baseurl'),
]
