# Generated by Django 2.2.12 on 2020-05-07 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(max_length=128)),
                ('assignee', models.CharField(max_length=100)),
                ('assignto', models.CharField(max_length=100)),
            ],
        ),
    ]
