# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-09 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactmessages', '0002_contactmessage_message_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='confirm_set',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
