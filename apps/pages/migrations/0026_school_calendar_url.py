# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-08 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0025_districtcalendaryear'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='calendar_url',
            field=models.URLField(blank=True, max_length=2048, null=True, verbose_name='School Calendar URL'),
        ),
    ]
