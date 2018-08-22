# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-11 15:14
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0020_auto_20180711_0613'),
        ('pages', '0036_page_about_our_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('title', models.CharField(db_index=True, max_length=200)),
                ('body', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('announcement_page_node', models.OneToOneField(db_column='announcement_page_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Page')),
                ('inline_order', models.PositiveIntegerField(db_index=True, default=0)),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pages_announcement_node', to='objects.Node')),
            ],
            options={
                'verbose_name_plural': 'Announcements',
                'verbose_name': 'Announcement',
                'permissions': (('trash_announcement', 'Can soft delete announcement'), ('restore_announcement', 'Can restore announcement')),
                'ordering': ['inline_order'],
                'get_latest_by': 'update_date',
                'default_manager_name': 'objects',
                'db_table': 'pages_announcement',
            },
            bases=('objects.page',),
        ),
    ]