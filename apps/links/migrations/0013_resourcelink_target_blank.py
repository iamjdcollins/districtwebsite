# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-07 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0012_resourcelink_modal_ajax'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcelink',
            name='target_blank',
            field=models.BooleanField(default=False),
        ),
    ]
