# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-27 14:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0011_generalsettings_monsido_domaintoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteType',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(help_text=('<span>Enter a name for this site type. The name should be a short descriptive name for the purpose of the site (e.g. ', ' School Website, District Website, or Teacher Website).</span>'), max_length=200, unique=True, verbose_name='Site Type')),
                ('create_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('update_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dashboard_sitetype_create_user', to=settings.AUTH_USER_MODEL, to_field='uuid')),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dashboard_sitetype_update_user', to=settings.AUTH_USER_MODEL, to_field='uuid')),
            ],
            options={
                'db_table': 'dashboard_sitetype',
                'verbose_name_plural': 'Site Types',
                'get_latest_by': 'update_date',
                'verbose_name': 'Site Type',
            },
        ),
    ]
