from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Clinic, NurseAssignment, NurseProfile

@receiver(post_save, sender=User)
def assign_nurse_to_default_clinic (sender, instance, created, **kwargs):
    if created and instance.role == 'nurse':
        default_clinic, _ = Clinic.objects.get_or_create(name='Default Clinic')
        NurseAssignment.objects.create(nurse=instance, clinic=default_clinic)

@receiver(post_save, sender=User)
def create_nurse_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'nurse':
        NurseProfile.objects.create(user=instance)