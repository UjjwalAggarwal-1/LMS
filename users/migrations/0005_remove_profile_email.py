# Generated by Django 4.0 on 2022-03-07 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_hostel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]
