# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-09 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactmessages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='message_sent',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
