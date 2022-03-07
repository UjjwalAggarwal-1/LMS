# Generated by Django 4.0 on 2022-03-07 11:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_books', '0022_alter_book_displayed_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='issued_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 7, 17, 8, 40, 500182), null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(0, 'No Review'), (1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], default=0, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='displayed_from',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 7, 17, 8, 40, 500182), null=True),
        ),
    ]
