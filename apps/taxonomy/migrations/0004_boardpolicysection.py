# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 21:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_node_has_permissions'),
        ('taxonomy', '0003_boardmeetingtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardPolicySection',
            fields=[
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Policy Section Name')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Policy Section Description')),
                ('section_prefix', models.CharField(blank=True, max_length=1, null=True)),
                ('boardpolicysection_taxonomy_node', models.OneToOneField(db_column='boardpolicysection_taxonomy_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Taxonomy')),
            ],
            options={
                'get_latest_by': 'update_date',
                'verbose_name_plural': 'Board Policy Sections',
                'verbose_name': 'Board Policy Section',
                'default_manager_name': 'objects',
                'db_table': 'taxonomy_boardpolicysection',
                'permissions': (('trash_boardpolicysection', 'Can soft delete board policy section'), ('restore_boardpolicysection', 'Can restore board policy section')),
            },
            bases=('objects.taxonomy',),
        ),
    ]