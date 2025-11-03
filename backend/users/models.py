from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('mother', 'Mother'),
        ('nurse', 'Nurse'),
    )
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    clinic = models.CharField(max_length=100, blank=True, null=True)  # For nurses
    email = models.EmailField(unique=True)
     
    def save(self, *args, **kwargs):
        if self.role == 'mother':
            self.clinic = None  # Ensure mothers don’t accidentally have a clinic
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.username} ({self.role})"
