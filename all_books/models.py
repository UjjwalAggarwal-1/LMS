from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

genre_choice = [('Action/Adventure', 'Action/Adventure'), ('Classics', 'Classics'),
                ('Comic Book/Graphic Novel', 'Comic Book/Graphic Novel'), ('Folklore', 'Folklore'),
                ('Detective/Mystery', 'Detective/Mystery'), ('Fantasy', 'Fantasy'),
                ('Historical Fiction', 'Historical Fiction'), ('Horror', 'Horror'),
                ('Literary Fiction', 'Literary Fiction'), ('Romance', 'Romance'),
                ('Science Fiction (Sci-Fi)', 'Science Fiction (Sci-Fi)'), ('Short Stories', 'Short Stories'),
                ('Suspense/Thrillers', 'Suspense/Thrillers'),
                ('Biographies/Autobiographies', 'Biographies/Autobiographies'),
                ('Cookbooks', 'Cookbooks'), ('History', 'History'),
                ('Poetry', 'Poetry'), ('Self-Growth', 'Self-Growth'), ('True Crime', 'True Crime')]


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
    published = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.title

    @property
    def num_issues(self):
        count = 0
        for issobj in Issue.objects.filter(isbn_of_book=self):
            if issobj.issued_on >= (timezone.now() - timezone.timedelta(days=90)):
                count += 1
        return '%d' % count


status_choices = [('pending', 'Pending'), ('issued', 'Issued'), ('returned', 'Returned'), ('rejected', 'Rejected'), ('renewed', 'Renewed')]
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
        return self.isbn_of_book.title, self.student.username


