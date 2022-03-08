from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    BITSID = models.CharField(max_length=16, default='null')
    mobile_num = models.CharField(max_length=15, verbose_name="Mobile/Contact number")
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
