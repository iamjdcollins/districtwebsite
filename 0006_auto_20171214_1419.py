# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

def set_inline_order(apps,schema_editor):
    Model = apps.get_model('links','resourcelink')
    for index, item in enumerate(Model.objects.all()):
        print('Setting ' + item.title + ' to an index of ' + str(index + 1))
        item.inline_order = index + 1
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0006_auto_20171214_1319'),
        ('links', '0005_auto_20171214_1319'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourcelink',
            options={'default_manager_name': 'objects', 'get_latest_by': 'update_date', 'ordering': ['inline_order'], 'permissions': (('trash_resourcelink', 'Can soft delete resource link'), ('restore_resourcelink', 'Can restore resource link')), 'verbose_name': 'Resource Link', 'verbose_name_plural': 'Resource Links'},
        ),
        migrations.RemoveField(
            model_name='resourcelink',
            name='related_nodes',
        ),
        migrations.AddField(
            model_name='resourcelink',
            name='inline_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='resourcelink',
            name='related_node',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='links_resourcelink_node', to='objects.Node'),
        ),
        migrations.RunPython(set_inline_order),
    ]
