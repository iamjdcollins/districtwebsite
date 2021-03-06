# Generated by Django 2.0 on 2018-08-30 16:15

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query_utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20180125_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, limit_choices_to=django.db.models.query_utils.Q(('content_type', 'school'), ('content_type', 'department'), _connector='OR'), null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users_employee_department', to='objects.Node'),
        ),
    ]
