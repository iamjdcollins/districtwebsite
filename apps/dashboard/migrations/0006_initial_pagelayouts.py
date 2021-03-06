# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-18 18:40
from __future__ import unicode_literals

from django.db import migrations


def create_initial_pagelayouts(apps, schema_editor):
    PageLayout = apps.get_model('dashboard', 'pagelayout')
    User = apps.get_model('objects', 'user')
    try:
        webmaster = User.objects.get(username='webmaster@slcschools.org')
    except User.DoesNotExist:
        webmaster = None
    pagelayout, created = PageLayout.objects.get_or_create(
        namespace='default.html',
    )
    pagelayout.title = 'Default'
    if created:
        pagelayout.create_user = webmaster
    pagelayout.update_user = webmaster
    pagelayout.save()
    pagelayout, created = PageLayout.objects.get_or_create(
        namespace='home.html',
    )
    pagelayout.title = 'Home Page'
    if created:
        pagelayout.create_user = webmaster
    pagelayout.update_user = webmaster
    pagelayout.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_pagelayout'),
    ]

    operations = [
        migrations.RunPython(create_initial_pagelayouts),
    ]
