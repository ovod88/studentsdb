# Generated by Django 2.0.5 on 2018-07-05 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_journal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='date',
            field=models.DateField(),
        ),
    ]
