# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 15:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_node_has_permissions'),
        ('documents', '0002_boardpolicy'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeProcedure',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('document_administrativeprocedure_node', models.OneToOneField(db_column='document_administrativeprocedure_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Document')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents_administrativeprocedure_node', to='objects.Node')),
            ],
            options={
                'verbose_name_plural': 'Administrative Procedures',
                'default_manager_name': 'objects',
                'permissions': (('trash_administrativeprocedure', 'Can soft delete administrative procedure'), ('restore_administrativeprocedure', 'Can restore administrative procedure')),
                'verbose_name': 'Administrative Procedure',
                'db_table': 'documents_administrativeprocedure',
                'get_latest_by': 'update_date',
            },
            bases=('objects.document',),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('document_policy_node', models.OneToOneField(db_column='document_policy_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Document')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents_policy_node', to='objects.Node')),
            ],
            options={
                'verbose_name_plural': 'Policies',
                'default_manager_name': 'objects',
                'permissions': (('trash_policy', 'Can soft delete policy'), ('restore_policy', 'Can restore policy')),
                'verbose_name': 'Policy',
                'db_table': 'documents_policy',
                'get_latest_by': 'update_date',
            },
            bases=('objects.document',),
        ),
        migrations.CreateModel(
            name='SupportingDocument',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('document_supportingdocument_node', models.OneToOneField(db_column='document_supportingdocument_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Document')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents_supportingdocument_node', to='objects.Node')),
            ],
            options={
                'verbose_name_plural': 'Supporting Documents',
                'default_manager_name': 'objects',
                'permissions': (('trash_supportingdocument', 'Can soft delete supporting document'), ('restore_supportingdocument', 'Can restore supporting document')),
                'verbose_name': 'Supporting Document',
                'db_table': 'documents_supportingdocument',
                'get_latest_by': 'update_date',
            },
            bases=('objects.document',),
        ),
    ]
