# Generated by Django 2.0.5 on 2018-07-05 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20180705_2142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journal',
            old_name='student_journal',
            new_name='student',
        ),
        migrations.AlterUniqueTogether(
            name='journal',
            unique_together={('student', 'date')},
        ),
    ]