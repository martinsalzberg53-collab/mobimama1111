import os

from django.core.management.base import BaseCommand
from django.db import transaction

from clinics.models import Clinic
from tips.models import Tip
from users.models import User

DEFAULT_TIPS = [
    {
        "title": "Drink plenty of water",
        "content": "Aim for about 8-10 glasses of water a day. Staying hydrated helps carry nutrients to your baby and prevents constipation.",
        "category": "NUTRITION",
    },
    {
        "title": "Take folic acid daily",
        "content": "Folic acid in the first trimester helps prevent neural tube defects. Your midwife can advise the right dose for you.",
        "category": "NUTRITION",
    },
    {
        "title": "Gentle walks are great",
        "content": "Moderate exercise like walking for 30 minutes most days supports a healthy pregnancy and easier delivery.",
        "category": "EXERCISE",
    },
    {
        "title": "Talk about how you feel",
        "content": "Pregnancy can bring big emotions. Sharing them with family, friends, or your clinic helps you stay well.",
        "category": "MENTAL_HEALTH",
    },
    {
        "title": "Watch for danger signs",
        "content": "Contact your clinic immediately if you have heavy bleeding, severe headache, blurry vision, or severe abdominal pain.",
        "category": "THIRD_TRIMESTER",
    },
]

DEFAULT_CLINICS = [
    {
        "name": "Korle-Bu Teaching Hospital",
        "address": "Guggisberg Avenue, Korle Bu, Accra",
        "phone_number": "0302 665 900",
    },
    {
        "name": "Komfo Anokye Teaching Hospital",
        "address": "Bantama, Kumasi",
        "phone_number": "0322 046 001",
    },
    {
        "name": "Ridge Hospital",
        "address": "Castle Road, Accra",
        "phone_number": "0302 661 761",
    },
]


class Command(BaseCommand):
    help = "Create the admin user and seed sample health tips (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        admin_email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
        admin_password = os.environ.get("ADMIN_PASSWORD", "")

        if admin_email and admin_password:
            admin, created = User.objects.get_or_create(
                email=admin_email,
                defaults={
                    "role": "ADMIN",
                    "is_staff": True,
                    "is_superuser": True,
                },
            )
            if created:
                admin.set_password(admin_password)
                admin.save()
                self.stdout.write(self.style.SUCCESS(f"Created admin user: {admin_email}"))
            else:
                self.stdout.write(self.style.WARNING(f"Admin user already exists: {admin_email}"))
        else:
            self.stdout.write(self.style.WARNING(
                "ADMIN_EMAIL / ADMIN_PASSWORD not set - skipping admin creation."
            ))

        if Tip.objects.count() == 0:
            admin = User.objects.filter(role="ADMIN").first()
            for tip_data in DEFAULT_TIPS:
                Tip.objects.create(
                    title=tip_data["title"],
                    content=tip_data["content"],
                    category=tip_data["category"],
                    author=admin,
                    is_approved=True,
                )
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(DEFAULT_TIPS)} sample health tips."))
        else:
            self.stdout.write(self.style.WARNING("Tips already exist - skipping seed."))

        if Clinic.objects.count() == 0:
            for clinic_data in DEFAULT_CLINICS:
                Clinic.objects.create(**clinic_data)
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(DEFAULT_CLINICS)} default clinics."))
        else:
            self.stdout.write(self.style.WARNING("Clinics already exist - skipping seed."))
