# Generated by Django 2.2.12 on 2020-05-07 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20200507_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
