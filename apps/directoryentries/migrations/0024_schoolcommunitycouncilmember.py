# Generated by Django 2.0 on 2018-09-26 21:00

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0024_auto_20180918_1055'),
        ('directoryentries', '0023_auto_20180918_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolCommunityCouncilMember',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('first_name', models.CharField(max_length=100, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, null=True, verbose_name='Last Name')),
                ('role', models.CharField(blank=True, max_length=100, null=True, verbose_name='Role')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Phone Number')),
                ('schoolcommunitycouncilmember_directoryentry_node', models.OneToOneField(db_column='schoolcommunitycouncilmember_directoryentry_node', editable=False, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='objects.DirectoryEntry')),
                ('inline_order', models.PositiveIntegerField(db_index=True, default=0)),
                ('related_node', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='directoryentries_schoolcommunitycouncilmember_node', to='objects.Node')),
            ],
            options={
                'verbose_name': 'School Community Council Member',
                'get_latest_by': 'create_date',
                'default_manager_name': 'base_manager',
                'db_table': 'directoryenties_schoolcommunitycouncilmember',
                'ordering': ['inline_order'],
                'verbose_name_plural': 'School Community Council Members',
            },
            bases=('objects.directoryentry',),
            managers=[
                ('base_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
