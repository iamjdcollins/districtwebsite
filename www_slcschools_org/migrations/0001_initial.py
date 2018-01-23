# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-22 19:01
from __future__ import unicode_literals

from django.db import migrations

def default_domain(apps, schema_editor):
    Site = apps.get_model('sites','Site')
    Alias = apps.get_model('multisite','Alias')
    site = Site.objects.get(pk=1)
    site.domain = 'www.slcschools.org'
    site.name = 'District Website'
    alias = site.aliases.first()
    alias.domain = 'www.slcschools.org'
    alias.save()
    alias, created = Alias.objects.get_or_create(domain='slcschools.org',is_canonical=None,redirect_to_canonical=True,site=site)
    alias.save()
    alias, created = Alias.objects.get_or_create(domain='www-test.slcschools.org',is_canonical=None,redirect_to_canonical=False,site=site)
    alias.save()
    alias, created = Alias.objects.get_or_create(domain='www-dev.slcschools.org',is_canonical=None,redirect_to_canonical=False,site=site)
    alias.save()
    site.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(default_domain),
    ]