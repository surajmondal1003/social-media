# Generated by Django 2.0.3 on 2018-04-23 10:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0008_auto_20180423_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 23, 10, 36, 41, 971077, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_date',
            field=models.DateField(default=datetime.datetime(2018, 4, 23, 10, 36, 41, 971077, tzinfo=utc)),
        ),
    ]
