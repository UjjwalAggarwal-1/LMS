# Generated by Django 4.0 on 2022-03-09 20:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('all_books', '0042_alter_book_displayed_from_alter_issue_issued_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='published',
            field=models.DateField(default=datetime.datetime(2022, 3, 9, 20, 0, 0, 348798, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='book',
            name='displayed_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 10, 1, 30, 0, 348798), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issued_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 10, 1, 30, 0, 348798), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='renewed_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 1, 30, 0, 364343), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='return_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 1, 30, 0, 348798), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='returned_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 1, 30, 0, 364343), null=True),
        ),
    ]