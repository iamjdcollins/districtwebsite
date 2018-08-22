# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-10 17:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0035_auto_20180702_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='about_our_school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_about_our_school', to='pages.School'),
        ),
    ]