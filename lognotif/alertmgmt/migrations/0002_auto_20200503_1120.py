# Generated by Django 2.2.12 on 2020-05-03 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertmgmt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtermodel',
            name='alarmFilter',
            field=models.TextField(default='-1', null=True),
        ),
        migrations.AlterField(
            model_name='filtermodel',
            name='severity',
            field=models.TextField(default='0', null=True),
        ),
    ]