# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-22 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactmessages', '0005_auto_20180222_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='http_headers',
            field=models.TextField(blank=True, null=True),
        ),
    ]
