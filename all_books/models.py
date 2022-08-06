from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

genre_choice = ('Action', 'Adventure', 'Classics', 'Comic Book', 'Graphic Novel', 'Folklore', 'Detective',
                'Horror', 'Literary Fiction', 'Romance', 'Science Fiction', 'Short Stories',
                'Suspense', 'Thrillers', 'Biographies', 'Autobiographies', 'Cookbooks', 'History', 'Poetry',
                'Mystery', 'Fantasy', 'Self Growth', 'True Crime')


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    isbn = models.IntegerField(verbose_name='ISBN')
    publisher = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre)
    location = models.CharField(max_length=20, default='unknown')
    displayed_from = models.DateTimeField(blank=True, null=True, default=timezone.now)
    availability = models.ManyToManyField(User, through='Issue')
    quantity = models.PositiveIntegerField()
    published = models.DateField(default=datetime.date.today())
    summary = models.TextField(max_length=500)

    @property
    def num_issues(self):
        count = 0
        for issobj in Issue.objects.filter(book=self):
            if issobj.issued_on >= (timezone.now() - timezone.timedelta(days=90)):
                count += 1
        return count

    @property
    def unique_num_issues(self):
        lastmonth = timezone.now() - timezone.timedelta(days=30)
        book = self
        count = 0
        student_list = []
        for issobj in Issue.objects.filter(book=book):
            if issobj.issued_on >= lastmonth:
                if issobj.student not in student_list:
                    count += 1
                    student_list.append(issobj.student)
        return count

    @property
    def genres_stringed(self):
        return '|'.join(self.genre.all().values_list('name', flat=True))

    def __str__(self):
        return self.title


status_choices = [('pending', 'Pending'), ('issued', 'Issued'), ('returned', 'Returned'), ('rejected', 'Rejected'),
                  ('renewed', 'Renewed')]
rating_choices = [(0, 'No Rating'), (1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')]


class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices, default='pending', null=True,
                              blank=True)
    reject_request = models.CharField(max_length=300, null=True, blank=True)
    return_on = models.DateTimeField(null=True, default=datetime.datetime.now() + datetime.timedelta(days=20))
    issued_on = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now())
    requested_on = models.DateTimeField(null=True, default=datetime.datetime.now())
    returned_on = models.DateTimeField(null=True, default=datetime.datetime.now())
    renewed_on = models.DateTimeField(null=True, default=datetime.datetime.now())
    rating = models.IntegerField(choices=rating_choices, default=0, blank=True, null=True)
    review = models.TextField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.book.title
