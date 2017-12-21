from django import template
from django.utils.safestring import mark_safe
import re
from apps.objects.models import Node

register = template.Library()

nodes = Node.objects.filter(node_type='pages').filter(content_type='department').only('pk','node_title','url')
nodes_dict = {}
for node in nodes:
    nodes_dict[str(node.pk)] = {'node_title': node.node_title,'url': node.url}

def linked(match,nodes=nodes_dict):
    if match.group(1) in nodes:
        title = nodes[match.group(1)]['node_title']
        url = nodes[match.group(1)]['url']
    else:
        title = match.group(2)
        url = match.group(1)
    value = '<a href="' + url  + '" class="relink linked" data-id="' + match.group(1) + '">' + match.group(2) + '</a>'
    return value

@register.filter(name='relink',is_safe=True)
def relink(value):
    value = re.sub(r'<a class=\"relink\" data-id=\"([a-z0-9-]+)\">(.*?)</a>',linked,value)
    return mark_safe(value)
