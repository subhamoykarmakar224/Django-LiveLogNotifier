# Generated by Django 2.2.12 on 2020-05-06 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertmgmt', '0010_auto_20200506_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='newassignment',
            name='loglist',
            field=models.TextField(default='ALL'),
        ),
    ]
