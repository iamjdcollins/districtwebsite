from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.BaseURL.as_view(), name='baseurl'),
  url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
  url(r'^general/$', views.GeneralSettings.as_view(), name='general'),
  url(r'^sites/$', views.Sites.as_view(), name='sites'),
  url(r'^sites/add/$', views.SitesAdd.as_view(), name='sitesadd'),
  url(r'^sites/change/(?P<sitepk>.*)/$', views.SitesChange.as_view(), name='siteschange'),
  url(r'^sitetypes/$', views.SiteTypes.as_view(), name='sitetypes'),
  url(r'^sitetypes/add/$', views.SiteTypesAdd.as_view(), name='sitetypesadd'),
  url(r'^sitetypes/change/(?P<sitetypepk>.*)/$', views.SiteTypesChange.as_view(), name='sitetypeschange'),
  url(r'^templates/$', views.Templates.as_view(), name='templates'),
  url(r'^templates/add/$', views.TemplatesAdd.as_view(), name='templatesadd'),
  url(r'^pagelayouts/$', views.PageLayouts.as_view(), name='pagelayouts'),
  url(r'^pagelayouts/add/$', views.PageLayoutsAdd.as_view(), name='pagelayoutsadd'),
  url(r'^pagelayouts/change/(?P<pagelayoutpk>.*)/$', views.PageLayoutsChange.as_view(), name='pagelayoutschange'),
]
