from .models import Node
import mptt
import apps.common.functions as commonfunctions

def breadcrumb(request):
    breadcrumb = Node.objects.filter(url=request.path).get_ancestors(include_self=True)
    return {'BREADCRUMB': breadcrumb}

def mainmenu(request):
  if request.site.domain == 'www.slcschools.org':
    menu_items = Node.objects.filter(menu_item=1).filter(level=0).filter(site=request.site).filter(published=1).filter(deleted=0)
  else:
    menu_items = []
    possible_menu_items = (
      Node
      .objects
      .filter(
        menu_item=1,
        level=0,
        site=request.site,
        published=1,
        deleted=0,
      )
    )
    for item in possible_menu_items:
      if (
          request.user.is_superuser or
          request.user.groups.filter(name='Website Managers') or
          request.site.dashboard_sitepublisher_site.filter(account=request.user.pk)
      ):
        menu_items.append(item)
      else:
        if len(
          item
          .get_children()
          .filter(
            node_type='pages',
            content_type='page',
            deleted=0,
            published=1,
          )
        ) > 0:
          menu_items.append(item)
  return {'MENU_ITEMS': menu_items}

def sitestructure(requset):
    sitestructure = Node.objects.all()
    return {'SITESTRUCTURE': sitestructure}

def is_siteadmin(request):
    return {'SITEADMIN': commonfunctions.is_siteadmin(request)}