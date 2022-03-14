from PIL import Image
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from all_books.models import Issue


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bits_id = models.CharField(max_length=16, default='null', verbose_name='BITS ID')
    mobile_num = models.PositiveIntegerField(max_length=15, verbose_name="Mobile/Contact number", validators=[
            MaxValueValidator(10), MinValueValidator(10)])
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    librarian = models.BooleanField(null=False, default=False)
    hostel = models.CharField(max_length=25, choices=
                            [('Srinivas Ramanujan', 'Srinivas Ramanujan'), ('Gandhi', 'Gandhi'),
                             ('Krishna', 'Krishna'), ('Meera', 'Meera')], default='unknown')
    room_no = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def merit_score(self):
        stu_iss_qs = Issue.objects.filter(student=self.user)
        tscore = 0
        tcount = stu_iss_qs.count()
        for data in stu_iss_qs:
            tscore += data.score
            if data.score == 0:
                tcount -= 1
        if tcount == 0:
            return 'no score yet'
        else:
            merit_score = tscore / tcount
            merit_score = round(merit_score, 3)
            return merit_score

    @property
    def total_issues(self):
        total_issues = Issue.objects.filter(student=self.user).count()
        return total_issues
