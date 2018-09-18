# Generated by Django 2.0 on 2018-09-18 16:55

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0002_auto_20171219_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'update_date', 'ordering': ['inline_order'], 'permissions': (('trash_faq', 'Can soft delete faq'), ('restore_faq', 'Can restore faq')), 'verbose_name': 'Fequently Asked Question', 'verbose_name_plural': 'Frequently Asked Questions'},
        ),
        migrations.AlterModelManagers(
            name='faq',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
