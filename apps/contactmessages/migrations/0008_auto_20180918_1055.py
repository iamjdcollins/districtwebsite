# Generated by Django 2.0 on 2018-09-18 16:55

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('contactmessages', '0007_contactmessage_message_to'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactmessage',
            options={'default_manager_name': 'base_manager', 'get_latest_by': 'update_date', 'ordering': ['inline_order'], 'permissions': (('trash_contactmessage', 'Can soft delete contact message'), ('restore_contactmessage', 'Can restore contact message')), 'verbose_name': 'Contact Message', 'verbose_name_plural': 'Contact Message'},
        ),
        migrations.AlterModelManagers(
            name='contactmessage',
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
