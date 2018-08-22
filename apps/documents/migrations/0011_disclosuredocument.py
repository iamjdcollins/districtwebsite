# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-22 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0020_auto_20180711_0613'),
        ('documents', '0010_auto_20180208_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisclosureDocument',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('disclosuredocument_document_node', models.OneToOneField(db_column='disclosuredocument_document_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Document')),
                ('inline_order', models.PositiveIntegerField(db_index=True, default=0)),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents_disclosuredocument_node', to='objects.Node')),
            ],
            options={
                'verbose_name': 'Disclosure Document',
                'get_latest_by': 'update_date',
                'permissions': (('trash_document', 'Can soft delete Disclosure Document'), ('restore_document', 'Can restore Disclosure Document')),
                'db_table': 'documents_disclosuredocument',
                'verbose_name_plural': 'Disclosure Documents',
                'ordering': ['inline_order'],
                'default_manager_name': 'objects',
            },
            bases=('objects.document',),
        ),
    ]
