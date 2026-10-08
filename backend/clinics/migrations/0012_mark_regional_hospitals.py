from django.db import migrations, models

# The 16 regional hospitals the platform presents (one per Ghana region).
# Names are unique across the dataset, so matching by name is safe.
REGIONAL_HOSPITALS = [
    "Korle-Bu Teaching Hospital",        # Greater Accra
    "Komfo Anokye Teaching Hospital",     # Ashanti
    "Effia Nkwanta Regional Hospital",    # Western
    "Wiawso Government Hospital",         # Western North
    "Cape Coast Teaching Hospital",       # Central
    "Eastern Regional Hospital",          # Eastern
    "Ho Teaching Hospital",               # Volta
    "Mary Theresa Hospital",              # Oti
    "Tamale Teaching Hospital",           # Northern
    "Damongo Government Hospital",        # Savannah
    "Baptist Medical Centre",             # North East
    "Bolgatanga Regional Hospital",       # Upper East
    "Nandom Municipal Hospital",          # Upper West
    "Sunyani Regional Hospital",          # Bono
    "Holy Family Teaching Hospital",      # Bono East
    "St. Elizabeth Hospital",             # Ahafo
]


def mark_regional(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    Clinic.objects.filter(name__in=REGIONAL_HOSPITALS).update(regional=True)


def unmark_regional(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    Clinic.objects.filter(name__in=REGIONAL_HOSPITALS).update(regional=False)


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0011_real_world_hospital_domains"),
    ]

    operations = [
        migrations.AddField(
            model_name="clinic",
            name="regional",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(mark_regional, unmark_regional),
    ]