# Generated by Django 4.0 on 2022-03-18 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_bitsid_remove_profile_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile_num',
            field=models.BigIntegerField(default='0', verbose_name='Mobile/Contact number'),
        ),
    ]
