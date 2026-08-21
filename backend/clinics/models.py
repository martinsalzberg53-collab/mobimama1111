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
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role':'nurse'})
    qualifications = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class NurseAssignment(models.Model):
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'nurse'})
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nurse.username} → {self.clinic.name}"