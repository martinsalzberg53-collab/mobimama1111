from django.db import models
from users.models import User  # Import the custom User model

# Create your models here.

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name
    
class NurseProfile(models.Model):

    REGISTRATION_TYPE_CHOICES = (
        ('PIN', 'NMC PIN (Nurse)'),
        ('AIN', 'AIN (Midwife)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nurse_profile', limit_choices_to={'role':'NURSE'})
    qualifications = models.TextField(blank=True)
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPE_CHOICES, default='PIN')

    def __str__(self):
        email = self.user.email if self.user_id else ''
        return f"{self.user.get_full_name() or email or self.user_id} ({self.registration_type})"

class AllowedHospitalDomain(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    hospital = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain

class NurseAssignment(models.Model):
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'nurse'})
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nurse.username} → {self.clinic.name}"