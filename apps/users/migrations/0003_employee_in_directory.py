# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171120_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='in_directory',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
