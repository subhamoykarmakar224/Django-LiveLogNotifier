# Generated by Django 2.2.12 on 2020-05-03 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertmgmt', '0004_logfilterfields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logfilterfields',
            old_name='severity_fields',
            new_name='timestamp_sort',
        ),
    ]
