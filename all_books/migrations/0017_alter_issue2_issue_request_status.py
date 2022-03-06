# Generated by Django 4.0 on 2022-03-06 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_books', '0016_alter_issue2_reject_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue2',
            name='issue_request_status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('issued', 'Issued'), ('returned', 'Returned'), ('rejected', 'Rejected')], default='pending', max_length=10, null=True),
        ),
    ]
