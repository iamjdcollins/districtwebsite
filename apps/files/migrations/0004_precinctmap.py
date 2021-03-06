# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-25 17:47
from __future__ import unicode_literals

import apps.common.functions
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0018_auto_20180419_1349'),
        ('files', '0003_auto_20171214_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrecinctMap',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('file_file', models.FileField(max_length=2000, upload_to=apps.common.functions.file_upload_to, verbose_name='File')),
                ('file_file_node', models.OneToOneField(db_column='precinctmap_file_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.File')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files_precinctmap_node', to='objects.Node')),
            ],
            options={
                'verbose_name': 'Precinct Map',
                'verbose_name_plural': 'Precinct Maps',
                'permissions': (('trash_precinctmap', 'Can soft delete precinct map'), ('restore_file', 'Can restore precinct map')),
                'get_latest_by': 'update_date',
                'db_table': 'files_precinctmap',
                'default_manager_name': 'objects',
            },
            bases=('objects.file',),
        ),
    ]
