# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-29 17:57
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0013_auto_20180125_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='slug',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
