# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directoryentries', '0010_administrator'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrator',
            name='job_title',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]