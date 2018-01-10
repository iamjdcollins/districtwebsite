# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-10 21:35
from __future__ import unicode_literals

from django.db import migrations, models

def set_inline_order(apps,schema_editor):
    Model = apps.get_model('pages','boardsubpage')
    for index, item in enumerate(Model.objects.all()):
        print('Setting ' + item.title + ' to an index of ' + str(index + 1))
        item.inline_order = index + 1
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0028_school_donate_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardsubpage',
            options={'default_manager_name': 'objects', 'get_latest_by': 'update_date', 'ordering': ['inline_order'], 'permissions': (('trash_boardsubpage', 'Can soft delete board subpage'), ('restore_boardsubpage', 'Can restore board subpage')), 'verbose_name': 'Board Subpage', 'verbose_name_plural': 'Board Subpages'},
        ),
        migrations.AddField(
            model_name='boardsubpage',
            name='inline_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.RunPython(set_inline_order),
    ]