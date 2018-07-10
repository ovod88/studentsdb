# Generated by Django 2.0.5 on 2018-07-10 14:55

from django.db import migrations, models
import django.db.models.deletion
import students.models.examin_results


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_auto_20180710_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Examin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Назва')),
                ('date', models.DateField()),
                ('examin_group', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Group', verbose_name='Група')),
                ('examin_professor', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Professor', verbose_name='Викладач')),
            ],
            options={
                'verbose_name': 'Екзамін',
                'verbose_name_plural': 'Екзаміни',
            },
        ),
        migrations.CreateModel(
            name='ExaminResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', students.models.examin_results.PositiveSmallIntegerFieldLimit()),
                ('examin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Examin', verbose_name='Екзамін')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Результат екзаміну',
                'verbose_name_plural': 'Результати екзаміну',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='student_examin',
            field=models.ManyToManyField(blank='False', through='students.ExaminResult', to='students.Examin', verbose_name='Екзамін'),
        ),
    ]
