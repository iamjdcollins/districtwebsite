# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-12 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0031_data_schooladminorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='school_number',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True, unique=True),
        ),
    ]
