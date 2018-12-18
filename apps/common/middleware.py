import os
from django.conf import settings
from django.views.decorators.cache import patch_cache_control


class DynamicDataDir(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        settings.DATA_DIR = '/srv/nginx/' + request.site.domain
        settings.MEDIA_ROOT = os.path.join(settings.DATA_DIR)
        settings.STATIC_ROOT = os.path.join(settings.MEDIA_ROOT, 'static')

        response = self.get_response(request)

        return response


class UserCacheControl(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_anonymous:
            patch_cache_control(response, public=True)
        else:
            patch_cache_control(response, private=True, no_cache=True)
            # patch_cache_control(response, no-cache=True)
        return response

