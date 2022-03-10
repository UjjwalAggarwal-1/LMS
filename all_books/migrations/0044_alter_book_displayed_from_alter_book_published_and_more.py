# Generated by Django 4.0 on 2022-03-10 04:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_books', '0043_book_published_alter_book_displayed_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='displayed_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 10, 10, 19, 42, 183477), null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='published',
            field=models.DateField(default=datetime.date(2022, 3, 10)),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issued_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 10, 10, 19, 42, 183477), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='renewed_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 10, 19, 42, 183477), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='return_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 10, 19, 42, 183477), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='returned_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 10, 19, 42, 183477), null=True),
        ),
    ]
