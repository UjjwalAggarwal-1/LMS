from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Issue
from django.core.mail import send_mail


@receiver(post_save, sender=Issue)
def send_issued_mail(sender, created, instance, **kwargs):
    if instance.status == 'issued':
        subject = "book issued successfully "
        send_mail(subject, 'Body', '12aujjwalbis.aggarwal@gmail.com', ['f20212427@pilani.bits-pilani.ac.in'], fail_silently=False,)
