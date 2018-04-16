from django.conf.urls import url

from . import views
from .models import Page

Pages = Page.objects.filter(deleted=0).filter(published=1)

urlpatterns = [
    url(r'^(?:[a-z0-9-]+\/)*$', views.node_lookup, name='node_lookup'),
]
