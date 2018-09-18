# Generated by Django 2.0 on 2018-09-18 16:55

import django.contrib.auth.models
from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0023_auto_20180830_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactmessage',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Contact Message', 'verbose_name_plural': 'Contact Messages'},
        ),
        migrations.AlterModelOptions(
            name='directoryentry',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Directory Entry', 'verbose_name_plural': 'Directory Entries'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='faq',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQs'},
        ),
        migrations.AlterModelOptions(
            name='file',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'File', 'verbose_name_plural': 'Files'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelOptions(
            name='link',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Link', 'verbose_name_plural': 'Links'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Page', 'verbose_name_plural': 'Pages'},
        ),
        migrations.AlterModelOptions(
            name='taxonomy',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Taxonomy', 'verbose_name_plural': 'Taxonomies'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelManagers(
            name='contactmessage',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='directoryentry',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='document',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='event',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='faq',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='file',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='image',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='link',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='page',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='taxonomy',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
