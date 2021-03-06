# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-22 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactmessages', '0004_auto_20180109_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='http_headers',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='our_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='remote_addr',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='user_agent',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
    ]
