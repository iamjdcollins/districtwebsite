# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-15 19:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_column='site_title', help_text='<p>Enter the title of the site.<br>It is recommended thisbe the official name of the entity this site represents.</p>', max_length=200, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('update_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dashboard_general_create_user', to=settings.AUTH_USER_MODEL, to_field='uuid')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='dashboard_general_site', to='sites.Site')),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dashboard_general_update_user', to=settings.AUTH_USER_MODEL, to_field='uuid')),
            ],
            options={
                'db_table': 'dashboard_generalsettings',
                'verbose_name': 'General Settings',
                'verbose_name_plural': 'General Settings',
                'get_latest_by': 'update_date',
            },
        ),
    ]
