# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 20:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0004_auto_20171214_1225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourcelink',
            options={'default_manager_name': 'objects', 'get_latest_by': 'update_date', 'permissions': (('trash_resourcelink', 'Can soft delete resource link'), ('restore_resourcelink', 'Can restore resource link')), 'verbose_name': 'Resource Link', 'verbose_name_plural': 'Resource Links'},
        ),
        migrations.AlterModelManagers(
            name='resourcelink',
            managers=[
            ],
        ),
    ]
