from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Clinic, NurseAssignment, NurseProfile


def _is_role(instance, role):
    return isinstance(instance.role, str) and instance.role.upper() == role


@receiver(post_save, sender=User)
def assign_nurse_to_default_clinic(sender, instance, created, **kwargs):
    if created and _is_role(instance, 'NURSE'):
        clinic = None
        if instance.clinic:
            clinic, _ = Clinic.objects.get_or_create(name=instance.clinic)
        else:
            clinic, _ = Clinic.objects.get_or_create(name='Default Clinic')
        NurseAssignment.objects.get_or_create(nurse=instance, clinic=clinic)


@receiver(post_save, sender=User)
def create_nurse_profile(sender, instance, created, **kwargs):
    if created and _is_role(instance, 'NURSE'):
        NurseProfile.objects.create(user=instance)