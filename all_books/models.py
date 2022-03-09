from django.db import models
from django.contrib.auth.models import User
import datetime


class Book(models.Model):
    title = models.CharField(max_length=100, default='none')
    author = models.CharField(max_length=50, default='none')
    publisher = models.CharField(max_length=50, default='none')
    genre = models.CharField(max_length=20, default='un-classified')
    summary = models.CharField(max_length=500, default='none')
    isbn = models.CharField(max_length=20)
    location = models.CharField(max_length=20, default='unknown')
    displayed_from = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now())
    availability = models.ManyToManyField(User, through='Issue')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title



status_choices = [("pending", 'Pending'), ('issued', 'Issued'), ('returned', 'Returned'), ('rejected', 'Rejected'), ('renewed', 'Renewed')]
rating_choices = [(0, 'No Rating'), (1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')]


class Issue(models.Model):
    isbn_of_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_request_status = models.CharField(max_length=10, choices=status_choices, default='pending', null=True, blank=True)
    reject_request = models.CharField(max_length=300, null=True, blank=True)
    return_on = models.DateTimeField(null=True, default=datetime.datetime.now() + datetime.timedelta(days=20))
    issued_on = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now())
    returned_on = models.DateTimeField(null=True, default=datetime.datetime.now())
    renewed_on = models.DateTimeField(null=True, default=datetime.datetime.now())
    rating = models.IntegerField(choices=rating_choices, default=0, blank=True, null=True)
    review = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.isbn_of_book.title
