# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 22:24
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0002_node_primary_contact'),
        ('pages', '0007_auto_20171129_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubPage',
            fields=[
                ('title', models.CharField(db_index=True, max_length=200)),
                ('body', ckeditor.fields.RichTextField(blank=True, help_text="<ol>  <li class='help'>    <p class='help'></p>  </li></ol>", null=True)),
                ('subpage_page_node', models.OneToOneField(db_column='subpage_page_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Page')),
            ],
            options={
                'verbose_name': 'Sub Page',
                'permissions': (('trash_subpage', 'Can soft delete subpage'), ('restore_subpage', 'Can restore subpage')),
                'db_table': 'pages_subpage',
                'get_latest_by': 'update_date',
                'verbose_name_plural': 'Sub Pages',
            },
            bases=('objects.page',),
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]