# Generated by Django 4.0 on 2022-03-13 20:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_books', '0055_issue_requested_on_alter_book_displayed_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='displayed_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 14, 1, 31, 10, 330347), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issued_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 14, 1, 31, 10, 330347), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='renewed_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 14, 1, 31, 10, 330347), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='requested_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 14, 1, 31, 10, 330347), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='return_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 3, 1, 31, 10, 330347), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='returned_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 14, 1, 31, 10, 330347), null=True),
        ),
    ]
