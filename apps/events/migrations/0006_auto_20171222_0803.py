# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-22 15:03
from __future__ import unicode_literals

import apps.common.functions
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0007_faq'),
        ('taxonomy', '0005_auto_20171214_1319'),
        ('events', '0005_auto_20171210_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictCalendarEvent',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('originaldate', models.DateTimeField(db_index=True, verbose_name='Original Start Date and Time')),
                ('originalinstance', models.PositiveIntegerField(blank=True, null=True)),
                ('event_name', models.CharField(blank=True, max_length=400, null=True)),
                ('startdate', models.DateTimeField(default=apps.common.functions.tomorrow_midnight, verbose_name='Start Date and Time')),
                ('enddate', models.DateTimeField(blank=True, null=True, verbose_name='End Date and Time')),
                ('schoolyear', models.CharField(max_length=7)),
                ('yearend', models.CharField(max_length=4)),
                ('non_district_location', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name of Non-District Location')),
                ('non_district_location_google_place', models.URLField(blank=True, max_length=2048, null=True, verbose_name='Name of Non-District Location Google Place')),
                ('cancelled', models.BooleanField(default=False)),
                ('districtcalendarevent_event_node', models.OneToOneField(db_column='districtcalendarevent_event_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Event')),
                ('building_location', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events_districtcalendarevent_build_location', to='taxonomy.Location')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events_districtcalendarevent_node', to='objects.Node')),
            ],
            options={
                'verbose_name': 'District Calendar Event',
                'permissions': (('trash_districtcalendarevent', 'Can soft delete district calendar event'), ('restore_districtcalendarevent', 'Can restore district calendar event')),
                'verbose_name_plural': 'District Calendar Events',
                'get_latest_by': 'update_date',
                'default_manager_name': 'objects',
                'db_table': 'events_districtcalendarevent',
            },
            bases=('objects.event',),
        ),
        migrations.AddField(
            model_name='boardmeeting',
            name='originalinstance',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
