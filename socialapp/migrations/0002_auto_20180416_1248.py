# Generated by Django 2.0.3 on 2018-04-16 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_personal',
            name='about_text',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user_personal',
            name='profilepic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
