# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_employee_in_directory'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='non_employee',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
