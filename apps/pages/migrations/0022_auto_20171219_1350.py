# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-19 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_auto_20171214_1319'),
        ('pages', '0021_auto_20171214_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='subpage',
            name='building_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pages_subpage_building_location', to='taxonomy.Location'),
        ),
        migrations.AddField(
            model_name='subpage',
            name='main_fax',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='subpage',
            name='main_phone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]