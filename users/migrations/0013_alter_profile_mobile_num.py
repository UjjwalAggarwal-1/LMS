# Generated by Django 4.0 on 2022-03-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_profile_mobile_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile_num',
            field=models.IntegerField(default='0', verbose_name='Mobile/Contact number'),
        ),
    ]