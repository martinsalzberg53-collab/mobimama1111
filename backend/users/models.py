from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
import datetime


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
        extra_fields.setdefault('email_verified', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('email_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    ROLE_CHOICES = (
        ('MOTHER', 'Mother'),
        ('NURSE', 'Nurse'),
        ('ADMIN', 'Admin'),
    )

    username = None
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    clinic = models.CharField(max_length=100, blank=True, null=True)

    nmc_pin = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.role != 'NURSE':
            self.clinic = None
        if self.role != 'NURSE':
            self.email_verified = True
        super().save(*args, **kwargs)

    def generate_otp(self):
        import random
        self.otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.otp_expires_at = timezone.now() + datetime.timedelta(minutes=7)
        self.save(update_fields=['otp_code', 'otp_expires_at'])

    def verify_otp(self, code):
        if self.otp_code != code:
            return False, "Invalid verification code."
        if timezone.now() > self.otp_expires_at:
            return False, "Verification code has expired. Please request a new one."
        self.email_verified = True
        self.otp_code = None
        self.otp_expires_at = None
        self.save(update_fields=['email_verified', 'otp_code', 'otp_expires_at'])
        return True, "Email verified successfully."

    def __str__(self):
        return f"{self.email} ({self.role})"