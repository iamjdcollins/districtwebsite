from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
import apps.thirdparty.django_saml2_auth.django_saml2_auth.views
from django.contrib.auth.views import logout
from apps.common.classes import CustomSearchView, CustomSearchForm
from haystack.views import SearchView
from django.http import HttpResponse
from socket import gethostname

urlpatterns = [
url(r'^saml_login/', include('apps.thirdparty.django_saml2_auth.django_saml2_auth.urls')),
url(r'^accounts/login/$', apps.thirdparty.django_saml2_auth.django_saml2_auth.views.signin),
url(r'^accounts/logout/$', logout,{'next_page': 'https://adfs.slcschools.org/adfs/ls/?wa=wsignout1.0&wreply=https://www.slcschools.org/'})
]

# Server Name


def servername(request):
    return HttpResponse('Server Online: {0}'.format(
        gethostname()
    ))


urlpatterns += [
    url(r'^server/$', servername, name='servername'),
]

# Dashboard App

urlpatterns += [
    url(r'^manage/', include('apps.dashboard.urls', namespace='dashboard')),
]

# Search Results
urlpatterns += [
    url(r'^search/results/', CustomSearchView.as_view(), name="haystack_search"),
]

# Media Library
urlpatterns += [
    url(r'^medialibrary/', include('apps.medialibrary.urls', namespace='medialibrary')),
]

admin.site.site_header = 'Salt Lake City School District'
admin.site.index_title = ('Salt Lake City School District')
admin.site.site_title = ('Salt Lake City School District')

urlpatterns += [
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^jet/', include('jet.urls', 'jet')),
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^backend/', admin.site.urls),
]

if settings.DEBUG and settings.ENVIRONMENT_MODE == 'development':
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Pages App Should be last since it matches all urls at the end.
urlpatterns += [
  url(r'', include('apps.pages.urls', namespace='pages')),
]
