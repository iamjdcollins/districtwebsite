# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-02 17:35
from __future__ import unicode_literals

import apps.common.functions
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_districtlogogroup_districtlogostylevariation'),
        ('objects', '0007_faq'),
        ('images', '0005_auto_20171214_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictLogo',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('districtlogo_image_node', models.OneToOneField(db_column='districtlogo_image_node', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='objects.Image')),
                ('district_logo_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images_districtlogo_district_logo_group', to='taxonomy.DistrictLogoGroup', verbose_name='District Logo Group')),
                ('district_logo_style_variation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images_districtlogo_district_logo_style_variation', to='taxonomy.DistrictLogoStyleVariation', verbose_name='District Logo Style Variation')),
                ('related_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_districtlogo_node', to='objects.Node')),
            ],
            options={
                'db_table': 'images_districtlogo',
                'get_latest_by': 'update_date',
                'default_manager_name': 'objects',
                'verbose_name': 'District Logo',
                'permissions': (('trash_districtlogo', 'Can soft delete district logo'), ('restore_districtlogo', 'Can restore district logo')),
                'verbose_name_plural': 'District Logos',
            },
            bases=('objects.image',),
        ),
        migrations.CreateModel(
            name='DistrictLogoGIF',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('image_file', models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image')),
                ('alttext', models.CharField(max_length=200, verbose_name='Alternative Text')),
                ('districtlogogif_image_node', models.OneToOneField(db_column='districtlogogif_image_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Image')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_districtlogogif_node', to='objects.Node')),
            ],
            options={
                'db_table': 'images_districtlogogif',
                'get_latest_by': 'update_date',
                'default_manager_name': 'objects',
                'verbose_name': 'District Logo GIF',
                'permissions': (('trash_districtlogogif', 'Can soft delete district logo gif'), ('restore_districtlogogif', 'Can restore district logo gif')),
                'verbose_name_plural': 'District Logo GIFs',
            },
            bases=('objects.image',),
        ),
        migrations.CreateModel(
            name='DistrictLogoJPG',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('image_file', models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image')),
                ('alttext', models.CharField(max_length=200, verbose_name='Alternative Text')),
                ('districtlogojpg_image_node', models.OneToOneField(db_column='districtlogojpg_image_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Image')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_districtlogojpg_node', to='objects.Node')),
            ],
            options={
                'db_table': 'images_districtlogojpg',
                'get_latest_by': 'update_date',
                'default_manager_name': 'objects',
                'verbose_name': 'District Logo JPG',
                'permissions': (('trash_districtlogojpg', 'Can soft delete district logo jpg'), ('restore_districtlogojpg', 'Can restore district logo jpg')),
                'verbose_name_plural': 'District Logo JPGs',
            },
            bases=('objects.image',),
        ),
        migrations.CreateModel(
            name='DistrictLogoPNG',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('image_file', models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image')),
                ('alttext', models.CharField(max_length=200, verbose_name='Alternative Text')),
                ('districtlogopng_image_node', models.OneToOneField(db_column='districtlogopng_image_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Image')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_districtlogopng_node', to='objects.Node')),
            ],
            options={
                'db_table': 'images_districtlogopng',
                'get_latest_by': 'update_date',
                'default_manager_name': 'objects',
                'verbose_name': 'District Logo PNG',
                'permissions': (('trash_districtlogopng', 'Can soft delete district logo png'), ('restore_districtlogopng', 'Can restore district logo png')),
                'verbose_name_plural': 'District Logo PNGs',
            },
            bases=('objects.image',),
        ),
        migrations.CreateModel(
            name='DistrictLogoTIF',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('image_file', models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image')),
                ('alttext', models.CharField(max_length=200, verbose_name='Alternative Text')),
                ('districtlogotif_image_node', models.OneToOneField(db_column='districtlogotif_image_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.Image')),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_districtlogotif_node', to='objects.Node')),
            ],
            options={
                'db_table': 'images_districtlogotif',
                'get_latest_by': 'update_date',
                'default_manager_name': 'objects',
                'verbose_name': 'District Logo TIF',
                'permissions': (('trash_districtlogotif', 'Can soft delete district logo tif'), ('restore_districtlogotif', 'Can restore district logo tif')),
                'verbose_name_plural': 'District Logo TIFs',
            },
            bases=('objects.image',),
        ),
    ]
