import os
from django.conf import settings


class DynamicDataDir(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        settings.DATA_DIR = '/srv/nginx/' + request.site.domain
        settings.MEDIA_ROOT = os.path.join(settings.DATA_DIR)
        settings.STATIC_ROOT = os.path.join(settings.MEDIA_ROOT, 'static')

        response = self.get_response(request)

        return response
