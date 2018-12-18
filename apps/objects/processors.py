from .models import Node
import mptt
import apps.common.functions as commonfunctions

def breadcrumb(request):
    breadcrumb = Node.objects.filter(url=request.path, site=request.site).get_ancestors(include_self=True)
    return {'BREADCRUMB': breadcrumb}

def mainmenu(request):
  if request.site.domain == 'www.slcschools.org':
    menu_items = Node.objects.filter(menu_item=1).filter(level=0).filter(site=request.site).filter(published=1).filter(deleted=0)
  else:
    menu_items = (
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
    if not commonfunctions.is_siteadmin(request):
        menu_items = menu_items.filter(section_page_count__gte=1)
  return {'MENU_ITEMS': menu_items}


def sitestructure(requset):
    sitestructure = Node.objects.all()
    return {'SITESTRUCTURE': sitestructure}


def is_siteadmin(request):
    return {'SITEADMIN': commonfunctions.is_siteadmin(request)}


def is_globaladmin(request):
    return {'GLOBALADMIN': commonfunctions.is_globaladmin(request)}
