# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]
