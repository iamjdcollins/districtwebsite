# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-11 12:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0019_auto_20180702_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='primary_contact',
            field=models.ForeignKey(blank=True, help_text='Optional: Primary Contact is used to specify who is responsible for receiving page feedback and other contact messages that were created on this page. Messages to specific people found in a directory listing on the page will still go to the appropriate person from the directory listing.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='objects_node_primary_contact', to=settings.AUTH_USER_MODEL, to_field='uuid'),
        ),
    ]
