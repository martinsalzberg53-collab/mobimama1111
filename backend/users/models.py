from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # You can add additional fields here if needed
    ROLE_CHOICES = (
        ('mother', 'Mother'),
        ('nurse', 'Nurse'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)