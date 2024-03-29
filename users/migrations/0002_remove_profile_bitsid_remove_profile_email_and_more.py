# Generated by Django 4.0 on 2022-03-17 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='BITSID',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AddField(
            model_name='profile',
            name='bits_id',
            field=models.CharField(default='null', max_length=16, verbose_name='BITS ID'),
        ),
        migrations.AddField(
            model_name='profile',
            name='hostel',
            field=models.CharField(choices=[('Srinivas Ramanujan', 'Srinivas Ramanujan'), ('Gandhi', 'Gandhi'), ('Krishna', 'Krishna'), ('Meera', 'Meera')], default='unknown', max_length=25),
        ),
        migrations.AddField(
            model_name='profile',
            name='librarian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='room_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_num',
            field=models.IntegerField(default='0', verbose_name='Mobile/Contact number'),
        ),
    ]
