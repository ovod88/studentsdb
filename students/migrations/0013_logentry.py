# Generated by Django 2.0.5 on 2018-09-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_auto_20180918_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_level', models.CharField(max_length=30, verbose_name='Log Level')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('module', models.CharField(max_length=100, verbose_name='Module')),
                ('message', models.TextField(verbose_name='Message')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
    ]
