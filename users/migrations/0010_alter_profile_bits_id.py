# Generated by Django 4.0 on 2022-03-14 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_mobile_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bits_id',
            field=models.CharField(default='null', max_length=16, verbose_name='BITS ID'),
        ),
    ]