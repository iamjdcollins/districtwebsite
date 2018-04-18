# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-18 17:14
from __future__ import unicode_literals

from django.db import migrations


def create_management_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Alias = apps.get_model('multisite', 'Alias')
    site, created = Site.objects.get_or_create(
        domain='websites.slcschools.org'
    )
    site.name = 'Website Management'
    site.save()
    alias, created = Alias.objects.get_or_create(
        domain='websites-dev.slcschools.org',
        is_canonical=None,
        redirect_to_canonical=False,
        site=site
    )
    alias.save()
    alias, created = Alias.objects.get_or_create(
        domain='websites-test.slcschools.org',
        is_canonical=None,
        redirect_to_canonical=False,
        site=site
    )
    alias.save()
    site.save()


def create_general_settings_all_sites(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    GeneralSettings = apps.get_model('dashboard', 'GeneralSettings')
    User = apps.get_model('objects', 'user')
    try:
        webmaster = User.objects.get(username='webmaster@slcschools.org')
    except User.DoesNotExist:
        webmaster = None
    for site in Site.objects.all():
        settings, created = GeneralSettings.objects.get_or_create(
            site=site
        )
        settings.title = site.name
        settings.primary_domain = site.domain
        if created:
            settings.create_user = webmaster
        settings.update_user = webmaster
        settings.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_management_site),
        migrations.RunPython(create_general_settings_all_sites),
    ]
