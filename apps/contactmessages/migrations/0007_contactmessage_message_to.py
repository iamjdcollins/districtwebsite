# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-01 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactmessages', '0006_auto_20180222_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='message_to',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
