# Generated by Django 4.2.5 on 2023-10-03 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_myuser_delete_timecode'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
