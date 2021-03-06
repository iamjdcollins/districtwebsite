# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 19:44
from __future__ import unicode_literals

from django.db import migrations, models

def set_inline_order(apps,schema_editor):
    Model = apps.get_model('documents','document')
    for index, item in enumerate(Model.objects.all()):
        print('Setting ' + item.title + ' to an index of ' + str(index + 1))
        item.inline_order = index + 1
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_boardmeetingagendaitem_boardmeetingexhibit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'get_latest_by': 'update_date', 'ordering': ['inline_order'], 'permissions': (('trash_document', 'Can soft delete document'), ('restore_document', 'Can restore document')), 'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AddField(
            model_name='document',
            name='inline_order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.RunPython(set_inline_order),
    ]
