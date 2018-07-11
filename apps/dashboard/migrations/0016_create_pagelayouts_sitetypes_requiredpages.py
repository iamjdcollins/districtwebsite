# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-09 14:00
from __future__ import unicode_literals

from django.db import migrations
from django.utils import timezone


def create_sitetypes(apps, schema_editor):
    SiteType = apps.get_model('dashboard', 'sitetype')
    User = apps.get_model('objects', 'user')
    webmaster = (
        User
        .objects
        .filter(username='webmaster@slcschools.org')
        .first()
    )
    sitetypes = ['District Website', 'School Website', ]
    for site in sitetypes:
        now = timezone.now()
        sitetype, created = SiteType.objects.get_or_create(
            title=site,
            defaults={
                'create_date': now,
                'create_user': webmaster,
                'update_date': now,
                'update_user': webmaster
            }
        )


def create_pagelayouts(apps, schema_editor):
    PageLayout = apps.get_model('dashboard', 'pagelayout')
    User = apps.get_model('objects', 'user')
    webmaster = (
        User
        .objects
        .filter(username='webmaster@slcschools.org')
        .first()
    )
    pagelayouts = {
        'about-our-school.html': 'About Our School',
        'administration-staff-directory.html': (
            'Administration & Staff Directory'
        ),
        'default.html': 'Default',
        'faculty-directory.html': 'Faculty Directory',
        'home.html': 'Home Page',
        'school-calendars.html': 'School Calendars',
        'search.html': 'Search',
        'school-athletics.html': 'School Athletics',
        'school-community.html': 'School Community',
        'school-students.html': 'School Students',
        'school-academics.html': 'School Academics',
        'school-employee-resources.html': 'School Employee Resources',
        'contact-us.html': 'Contact Us',
    }
    for namespace, title in pagelayouts.items():
        now = timezone.now()
        pagelayout, created = PageLayout.objects.get_or_create(
            namespace=namespace,
            defaults={
                'title': title,
                'create_date': now,
                'create_user': webmaster,
                'update_date': now,
                'update_user': webmaster
            }
        )
        pagelayout.title = title
        pagelayout.save()


def assign_pagelayouts(apps, schema_editor):
    SiteType = apps.get_model('dashboard', 'sitetype')
    PageLayout = apps.get_model('dashboard', 'pagelayout')
    pagelayouts = {
        'about-our-school.html': ['School Website', ],
        'administration-staff-directory.html': ['School Website', ],
        'default.html': ['District Website', 'School Website', ],
        'faculty-directory.html': ['School Website', ],
        'home.html': ['District Website', 'School Website', ],
        'school-calendars.html': ['School Website', ],
        'search.html': ['District Website', 'School Website', ],
        'school-athletics.html': ['School Website', ],
        'school-community.html': ['School Website', ],
        'school-students.html': ['School Website', ],
        'school-academics.html': ['School Website', ],
        'school-employee-resources.html': ['School Website', ],
        'contact-us.html': ['District Website', 'School Website', ],
    }
    for pagelayout in PageLayout.objects.all():
        for sitetype in SiteType.objects.all():
            if sitetype.title in pagelayouts[pagelayout.namespace]:
                pagelayout.allowed_sitetypes.add(sitetype)


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_generalsettings_sitetype'),
    ]

    operations = [
        migrations.RunPython(create_sitetypes),
        migrations.RunPython(create_pagelayouts),
        migrations.RunPython(assign_pagelayouts),
    ]
