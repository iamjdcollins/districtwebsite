# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-27 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_news_newsyear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='main_fax',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='main_phone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
