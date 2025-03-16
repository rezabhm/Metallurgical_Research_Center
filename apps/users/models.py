import random
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from configs.settings.base import verify_limit_time


# Create your models here.
class CustomUser(AbstractUser):

    phone_number = models.CharField(max_length=12)
    role = models.CharField(max_length=10, choices=(

        ('admin', 'admin'),
        ('customer', 'customer'),

    ))

    is_signup = models.BooleanField(default=False)

    otp_code = models.CharField(max_length=6, default='000000')
    otp_send_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    def generate_otp_code(self):

        """ generate new otp code """
        code = ''.join([str(random.randint(0,9)) for _ in range(6)])

        self.otp_code = code
        self.otp_send_time = timezone.now()
        self.save()

    def verify_otp_code(self, code):

        """ verify code """

        # if code successfully verified return 1 , if sent after limit time return -1 , if didn't math code return 0
        if timezone.now() > (self.otp_send_time + timedelta(minutes=verify_limit_time)):

            return -1

        elif self.otp_code == code:

            return 1

        else:

            return 0
