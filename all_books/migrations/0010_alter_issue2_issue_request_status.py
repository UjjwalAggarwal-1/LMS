# Generated by Django 4.0 on 2022-03-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_books', '0009_alter_issue2_issue_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue2',
            name='issue_request_status',
            field=models.CharField(choices=[('1', 'keep issued'), ('', 'return')], default='', max_length=10, null=True),
        ),
    ]
