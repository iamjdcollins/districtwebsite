# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-20 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0023_auto_20171220_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='is_department',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]