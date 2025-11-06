from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN') # Automatically set role to ADMIN

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('MOTHER', 'Mother'),
        ('NURSE', 'Nurse'),
        ('ADMIN', 'Admin'), # <-- ADDED ADMIN
    )
    
    # We don't need a username, we will use email to log in
    username = None 
    email = models.EmailField(unique=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    clinic = models.CharField(max_length=100, blank=True, null=True)

    # Tell Django to use 'email' as the login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # No other fields required (email and password are)

    objects = UserManager() # Use our new manager

    def save(self, *args, **kwargs):
        # If user is not a nurse, they can't have a clinic
        if self.role != 'NURSE':
            self.clinic = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.role})"