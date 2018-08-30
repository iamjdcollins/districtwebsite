# Generated by Django 2.0 on 2018-08-30 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_precinctmap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_language',
            field=models.ForeignKey(limit_choices_to={'deleted': False}, on_delete=django.db.models.deletion.PROTECT, related_name='files_file_file_language', to='taxonomy.Language'),
        ),
    ]
