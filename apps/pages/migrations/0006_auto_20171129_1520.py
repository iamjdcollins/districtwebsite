# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 22:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20171127_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='page_ptr',
            field=models.OneToOneField(db_column='news_page_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Page'),
        ),
        migrations.AlterField(
            model_name='newsyear',
            name='page_ptr',
            field=models.OneToOneField(db_column='newsyear_page_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Page'),
        ),
    ]
