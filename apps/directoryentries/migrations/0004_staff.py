# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
        ('users', '0001_initial'),
        ('directoryentries', '0003_auto_20171116_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('staff_directoryentry_node', models.OneToOneField(db_column='staff_directoryentry_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.DirectoryEntry')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directoryenties_staff_employee', to='users.Employee')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='directoryentries_staff_node', to='objects.Node')),
            ],
            options={
                'db_table': 'directoryenties_staff',
                'verbose_name': 'Staff',
                'default_manager_name': 'objects',
                'get_latest_by': 'create_date',
                'verbose_name_plural': 'Staff',
            },
            bases=('objects.directoryentry',),
        ),
    ]
