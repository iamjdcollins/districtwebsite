# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 21:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_auto_20171214_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourcelink',
            name='related_nodes',
        ),
    ]
