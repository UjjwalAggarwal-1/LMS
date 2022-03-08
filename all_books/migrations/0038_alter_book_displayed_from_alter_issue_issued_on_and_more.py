# Generated by Django 4.0 on 2022-03-08 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_books', '0037_alter_book_displayed_from_alter_issue_issued_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='displayed_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 8, 20, 58, 6, 218517), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issued_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 8, 20, 58, 6, 218517), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='renewed_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 8, 20, 58, 6, 218517), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='return_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 28, 20, 58, 6, 218517), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='returned_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 8, 20, 58, 6, 218517), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
