# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-20 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_auto_20171219_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='main_phone',
            field=models.CharField(default='18015780000', max_length=11),
        ),
    ]
