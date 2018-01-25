# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-23 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('objects', '0011_auto_20180123_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='url',
            field=models.CharField(db_index=True, max_length=2000),
        ),
        migrations.AlterUniqueTogether(
            name='node',
            unique_together=set([('site', 'url')]),
        ),
    ]