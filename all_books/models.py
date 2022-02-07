from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Books(models.Model):
    title = models.CharField(max_length=100, default='none')
    author = models.CharField(max_length=50, default='none')
    publisher = models.CharField(max_length=50, default='none')
    #genre = models.CharField(max_length=20, default='none')
    summary = models.CharField(max_length=500, default='none')
    ISBN = models.IntegerField()
    #location = models.CharField(max_length=20, default='none')
    #displayed_from = models.DateTimeField(default=timezone.now())

    availability = models.ForeignKey(User, on_delete=models.CASCADE)
    #quantity = models.IntegerField()

    def __str__(self):
        return self.title
