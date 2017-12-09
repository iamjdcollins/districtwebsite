# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 21:35
from __future__ import unicode_literals

import apps.common.functions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_boardmeeting_originaldate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardmeeting',
            name='startdate',
            field=models.DateTimeField(default=apps.common.functions.next_tuesday_sixthrity, verbose_name='Start Date and Time'),
        ),
    ]
