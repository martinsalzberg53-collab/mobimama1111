from django.db import models

# Create your models here.

from users.models import User  # Import the custom User model
from clinics.models import Clinic

class MotherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    clinic_name = models.CharField(max_length=100, blank=True, null=True)  # MVP: clinic as string
    health_info = models.JSONField(default=dict, blank=True)  # vitals, symptoms, AI data
    ai_insights = models.JSONField(default=dict, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_risk_reasons(self):
        reasons = []
        info = self.health_info or {}

        systolic = info.get('blood_pressure_systolic')
        diastolic = info.get('blood_pressure_diastolic')
        heart_rate = info.get('heart_rate')
        temperature = info.get('temperature')
        symptoms = info.get('symptoms', []) or []
        fetal_movement = info.get('fetal_movement')

        if systolic is not None and systolic >= 140:
            reasons.append('High systolic blood pressure')
        if diastolic is not None and diastolic >= 90:
            reasons.append('High diastolic blood pressure')
        if heart_rate is not None and heart_rate >= 100:
            reasons.append('Elevated heart rate')
        if temperature is not None and temperature >= 37.8:
            reasons.append('Fever detected')
        if 'severe_pain' in symptoms or 'heavy_bleeding' in symptoms:
            reasons.append('Serious reported symptoms')
        if fetal_movement is not None and fetal_movement == 'reduced':
            reasons.append('Reduced fetal movement')

        return reasons

    def get_risk_level(self):
        reasons = self.get_risk_reasons()
        if not reasons:
            return 'Low'

        info = self.health_info or {}
        systolic = info.get('blood_pressure_systolic')
        diastolic = info.get('blood_pressure_diastolic')
        heart_rate = info.get('heart_rate')
        temperature = info.get('temperature')
        symptoms = info.get('symptoms', []) or []

        if any([
            systolic is not None and systolic >= 160,
            diastolic is not None and diastolic >= 100,
            heart_rate is not None and heart_rate >= 110,
            temperature is not None and temperature >= 38.5,
            'heavy_bleeding' in symptoms,
            'severe_pain' in symptoms,
        ]):
            return 'High'

        return 'Medium'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"
