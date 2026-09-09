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

    LICENSE_STATUS_CHOICES = (
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nurse_profile', limit_choices_to={'role':'NURSE'})
    qualifications = models.TextField(blank=True)
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPE_CHOICES, default='PIN')
    license_file = models.FileField(upload_to='nurse_licenses/', blank=True, null=True)
    license_status = models.CharField(max_length=20, choices=LICENSE_STATUS_CHOICES, default='PENDING')
    license_extracted = models.JSONField(default=dict, blank=True)
    license_review_note = models.TextField(blank=True)

    def __str__(self):
        email = self.user.email if self.user_id else ''
        return f"{self.user.get_full_name() or email or self.user_id} ({self.registration_type})"

class NurseAssignment(models.Model):
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'nurse'})
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nurse.username} → {self.clinic.name}"