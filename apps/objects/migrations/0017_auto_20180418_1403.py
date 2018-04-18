# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-18 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def set_default_pagelayouts(apps, schema_editor):
    Node = apps.get_model('objects', 'node')
    PageLayout = apps.get_model('dashboard', 'pagelayout')
    default = PageLayout.objects.get(title='Default')
    for node in Node.objects.all():
        node.pagelayout = default
        node.save()


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0016_node_pagelayout'),
    ]

    operations = [
        migrations.RunPython(set_default_pagelayouts),
        migrations.AlterField(
            model_name='node',
            name='pagelayout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.PageLayout'),
        ),
    ]
