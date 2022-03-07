from django.db import models
from django.contrib.auth.models import User
import datetime


class Book(models.Model):
    title = models.CharField(max_length=100, default='none')
    author = models.CharField(max_length=50, default='none')
    publisher = models.CharField(max_length=50, default='none')
    #genre = models.CharField(max_length=20, default='none')
    summary = models.CharField(max_length=500, default='none')
    isbn = models.CharField(max_length=20)
    #location = models.CharField(max_length=20, default='none')
    displayed_from = models.DateTimeField(blank=True, null=True, default=datetime.date.today)

    availability = models.ManyToManyField(User, through='Issue')
    quantity = models.IntegerField()

    def __str__(self):
        return self.title


class Issue(models.Model):
    isbn_of_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    return_on = models.DateField(null=True, default=datetime.date.today()+datetime.timedelta(days=20))
    issue_request_status = models.CharField(max_length=10, choices=[
                ("pending", 'Pending'), ('issued', 'Issued'), ('returned', 'Returned'), ('rejected', 'Rejected')
                ], default='pending', null=True, blank=True)
    reject_request = models.CharField(max_length=300, null=True, blank=True)
