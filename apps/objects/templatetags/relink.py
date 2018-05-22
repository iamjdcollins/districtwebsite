from django import template
from django.utils.safestring import mark_safe
import re
from apps.objects.models import Node

register = template.Library()

nodes = Node.objects.all().only('pk', 'node_title', 'url')
nodes_dict = {}
for node in nodes:
    nodes_dict[str(node.pk)] = {'node_title': node.node_title, 'url': node.url}


def linked(match, nodes=nodes_dict):
    value = match.group(1)
    if re.search('relink', match.group(1)):
        try:
            id = re.search(r'data-id=\"(.*?)\"', match.group(1)).group(1)
        except IndexError:
            return ''
        if id in nodes:
            url = nodes[id]['url']
        else:
            url = False
        if url:
            value = re.sub(r'href=\".*?\"', 'href="{0}"'.format(url), value)
        value = re.sub(r'relink', 'relink linked', value)
    value = '<a {0}</a>'.format(value)
    return value


def images(match, nodes=nodes_dict):
    value = match.group(1)
    if re.search('inlineimage-img', match.group(1)):
        try:
            id = re.search(r'data-id=\"(.*?)\"', match.group(1)).group(1)
        except IndexError:
            return ''
        if id in nodes:
            url = nodes[id]['url']
        else:
            url = False
        if url:
            value = re.sub(r'src=\".*?\"', 'src="{0}"'.format(url), value)
        value = re.sub(r'inlineimage-img', 'inlineimage-img linked', value)
    value = '<img {0} />'.format(value)
    return value


@register.filter(name='relink', is_safe=True)
def relink(value):
    value = re.sub(r'<a (.*?)</a>', linked, value)
    value = re.sub(r'<img (.*?) />', images, value)
    return mark_safe(value)
