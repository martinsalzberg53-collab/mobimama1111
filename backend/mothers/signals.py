from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import MotherProfile


@receiver(post_save, sender=User)
def create_mother_profile(sender, instance, created, **kwargs):
    if created and isinstance(instance.role, str) and instance.role.upper() == 'MOTHER':
        MotherProfile.objects.create(user=instance)
