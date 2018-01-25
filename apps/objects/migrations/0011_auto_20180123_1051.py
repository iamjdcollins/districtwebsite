# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-23 17:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0010_node_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
    ]