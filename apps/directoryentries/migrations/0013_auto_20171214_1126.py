# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 18:26
from __future__ import unicode_literals

from django.db import migrations, models

def set_inline_order(apps,schema_editor):
    Staff = apps.get_model('directoryentries','staff')
    for index, item in enumerate(Staff.objects.all()):
        print('Setting ' + item.title + ' to an index of ' + str(index + 1))
        item.inline_order = index + 1
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('directoryentries', '0012_auto_20171214_1029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staff',
            options={'default_manager_name': 'objects', 'get_latest_by': 'create_date', 'ordering': ['inline_order'], 'verbose_name': 'Staff', 'verbose_name_plural': 'Staff'},
        ),
        migrations.AddField(
            model_name='staff',
            name='inline_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.RunPython(set_inline_order),
    ]