# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-09 22:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directoryentries', '0015_auto_20180205_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardmember',
            name='is_president',
            field=models.BooleanField(db_index=True, default=False, verbose_name='President'),
        ),
        migrations.AddField(
            model_name='boardmember',
            name='is_vicepresident',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Vice President'),
        ),
    ]
