# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-23 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_sitepublisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitepublisher',
            name='site',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='dashboard_sitepublisher_site', to='sites.Site'),
        ),
    ]
