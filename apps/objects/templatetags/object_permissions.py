from django import template
from apps.common.functions import has_change_permission

register = template.Library()


@register.simple_tag
def has_change_permissions(request, page):
    return has_change_permission(self=None, request=request, obj=page)
