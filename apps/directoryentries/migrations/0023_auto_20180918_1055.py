# Generated by Django 2.0 on 2018-09-18 16:55

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('directoryentries', '0022_auto_20180830_1015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrator',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'ordering': ['inline_order'], 'verbose_name': 'Administrator', 'verbose_name_plural': 'Administrators'},
        ),
        migrations.AlterModelOptions(
            name='boardmember',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Board Member', 'verbose_name_plural': 'Board Members'},
        ),
        migrations.AlterModelOptions(
            name='boardpolicyadmin',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Board Policy Administrator', 'verbose_name_plural': 'Board Policy Administrators'},
        ),
        migrations.AlterModelOptions(
            name='schooladministration',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'ordering': ['inline_order'], 'verbose_name': 'School Administrator', 'verbose_name_plural': 'School Administration'},
        ),
        migrations.AlterModelOptions(
            name='schooladministrator',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'ordering': ['inline_order'], 'verbose_name': 'School Administrator', 'verbose_name_plural': 'School Administrators'},
        ),
        migrations.AlterModelOptions(
            name='schoolfaculty',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'ordering': ['inline_order'], 'verbose_name': 'School Faculty', 'verbose_name_plural': 'School Faculty'},
        ),
        migrations.AlterModelOptions(
            name='schoolstaff',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'ordering': ['inline_order'], 'verbose_name': 'School Staff', 'verbose_name_plural': 'School Staff'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'ordering': ['inline_order'], 'verbose_name': 'Staff', 'verbose_name_plural': 'Staff'},
        ),
        migrations.AlterModelOptions(
            name='studentboardmember',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'create_date', 'verbose_name': 'Student Board Member', 'verbose_name_plural': 'Student Board Members'},
        ),
        migrations.AlterModelManagers(
            name='administrator',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='boardmember',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='boardpolicyadmin',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='schooladministration',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='schooladministrator',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='schoolfaculty',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='schoolstaff',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='staff',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='studentboardmember',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]