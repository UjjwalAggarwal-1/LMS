# Generated by Django 4.0 on 2022-03-08 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_merit_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='merit_score',
        ),
    ]