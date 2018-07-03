from django.core.management.base import BaseCommand
from apps.dashboard.models import GeneralSettings
from apps.pages.models import Page


def createpage(site, requiredpage, parents, remaining):
    if requiredpage in remaining:
        if requiredpage.parent:
            print('Page Has Parent')
            parents, remaining = createpage(
                site,
                requiredpage.parent,
                parents,
                remaining
            )
        if str(requiredpage.pk) in parents:
            parent = parents[str(requiredpage.pk)]
        else:
            parent = None
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
        print('{0} was created: {1}'.format(page, created))
        page.title = requiredpage.title
        page.menu_item = requiredpage.menu_item
        page.menu_title = requiredpage.menu_title
        page.pagelayout = requiredpage.pagelayout
        page.parent = parent
        page.site = site.site
        page.save()
        parents[str(page.pk)] = page
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
                    print('Creating: {0} for site: {1}'.format(
                        remaining[0],
                        site.title
                        )
                    )
                    parents, remaining = createpage(
                        site,
                        remaining[0],
                        parents,
                        remaining
                    )
