# Generated by Django 4.0 on 2022-03-01 16:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('all_books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_on', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('issue_request_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='books',
            name='ISBN',
        ),
        migrations.AddField(
            model_name='books',
            name='displayed_from',
            field=models.DateTimeField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='isbn',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='books',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='books',
            name='availability',
        ),
        migrations.AddField(
            model_name='books',
            name='availability',
            field=models.ManyToManyField(through='all_books.Issue2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issue2',
            name='isbn_of_book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='all_books.books'),
        ),
        migrations.AddField(
            model_name='issue2',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]