# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 19:37
from __future__ import unicode_literals

from django.db import migrations, models

def set_inline_order(apps,schema_editor):
    Model = apps.get_model('images','contentbanner')
    for index, item in enumerate(Model.objects.all()):
        print('Setting ' + item.title + ' to an index of ' + str(index + 1))
        item.inline_order = index + 1
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_profilepicture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentbanner',
            options={'default_manager_name': 'objects', 'get_latest_by': 'update_date', 'ordering': ['inline_order'], 'permissions': (('trash_contentbanner', 'Can soft delete content banner'), ('restore_contentbanner', 'Can restore content banner')), 'verbose_name': 'Content Banner', 'verbose_name_plural': 'Content Banners'},
        ),
        migrations.AddField(
            model_name='contentbanner',
            name='inline_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.RunPython(set_inline_order),
    ]
