# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-09 18:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactmessages', '0003_contactmessage_confirm_set'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='confirm_set',
            new_name='confirm_sent',
        ),
    ]