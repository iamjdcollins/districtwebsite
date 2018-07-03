from django.core.management.base import BaseCommand
from apps.dashboard.models import GeneralSettings
from apps.pages.models import Page


def createpage(site, requiredpage, parents, remaining):
    if requiredpage in remaining:
        parent = None
        if requiredpage.parent:
            parents, remaining = createpage(
                site,
                requiredpage.parent,
                parents,
                remaining
            )
            if str(requiredpage.parent.pk) in parents:
                parent = parents[str(requiredpage.parent.pk)]
        page, created = Page.objects.get_or_create(
            requiredpage=requiredpage,
            site=site.site,
            defaults={
                'title': requiredpage.title,
                'menu_item': requiredpage.menu_item,
                'menu_title': requiredpage.menu_title,
                'pagelayout': requiredpage.pagelayout,
                'parent': parent,
            }
        )
        if not created:
            changed = False
            if page.title != requiredpage.title:
                page.title = requiredpage.title
                changed = True
            if page.menu_item != requiredpage.menu_item:
                page.menu_item = requiredpage.menu_item
                changed = True
            if page.menu_title != requiredpage.menu_title:
                page.menu_title = requiredpage.menu_title
                changed = True
            if page.pagelayout != requiredpage.pagelayout:
                page.pagelayout = requiredpage.pagelayout
                changed = True
            if page.parent != parent:
                page.parent = parent
                changed = True
            if changed:
                page.save()
        parents[str(requiredpage.pk)] = page
        if page.requiredpage in remaining:
            remaining.remove(page.requiredpage)
    return parents, remaining


class Command(BaseCommand):
    def handle(self, *args, **options):
        for site in GeneralSettings.objects.all():
            if site.sitetype:
                parents = {}
                remaining = []
                for requiredpage in (
                    site.sitetype.dashboard_sitetyperequiredpage_sitetype.all()
                ):
                    remaining.append(requiredpage)
                while len(remaining) > 0:
                    parents, remaining = createpage(
                        site,
                        remaining[0],
                        parents,
                        remaining
                    )
