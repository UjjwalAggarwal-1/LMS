# Generated by Django 4.0 on 2022-03-07 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_hostel_profile_room_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hostel',
            field=models.CharField(choices=[('Srinivas Ramanujan', 'Srinivas Ramanujan'), ('Gandhi', 'Gandhi'), ('Krishna', 'Krishna'), ('Meera', 'Meera')], default='unknown', max_length=25),
        ),
    ]