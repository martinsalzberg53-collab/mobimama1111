from django.db import models

# Create your models here.
from users.models import User
from mothers.models import MotherProfile
from clinics.models import Clinic


class Appointment(models.Model):
    mother = models.ForeignKey(MotherProfile, on_delete=models.CASCADE)
    nurse = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role':'nurse'})
    clinic_name = models.ForeignKey(Clinic, on_delete=models.SET_NULL, blank=True, null=True)
    date_time = models.DateTimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=(('pending','Pending'), ('approved','Approved'), ('cancelled','Cancelled'), ('completed','Completed')),
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment: {self.mother.user.username} with {self.nurse.username if self.nurse else 'TBD'}"