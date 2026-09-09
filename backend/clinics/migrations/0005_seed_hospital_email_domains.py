from django.db import migrations


HOSPITAL_DOMAINS = [
    ("garh.gov.gh", "Greater Accra Regional Hospital (Ridge)"),
    ("erh.gov.gh", "Eastern Regional Hospital, Koforidua"),
    ("enrh.gov.gh", "Effia Nkwanta Regional Hospital, Takoradi"),
    ("brh.gov.gh", "Sunyani Regional Hospital"),
    ("urh.gov.gh", "Regional Hospital, Bolgatanga"),
    ("ashrh.gov.gh", "Sewua Regional Hospital (New Regional)"),
    ("crh.gov.gh", "Central Regional Hospital, Cape Coast"),
    ("vrh.gov.gh", "Ho Municipal Hospital (Acting Regional)"),
    ("nrh.gov.gh", "Tamale Regional Hospital"),
    ("uwrh.gov.gh", "Upper West Regional Hospital, Wa"),
    ("wnrh.gov.gh", "Wiawso Government Hospital (Acting)"),
    ("ahrh.gov.gh", "Goaso Government Hospital (Acting)"),
    ("berh.gov.gh", "Techiman Holy Family Hospital (Quasi/Acting)"),
    ("orh.gov.gh", "Worawora Government Hospital (Acting)"),
    ("srh.gov.gh", "Damongo Government Hospital (Acting)"),
    ("nerh.gov.gh", "Walewale Government Hospital (Acting)"),
    ("kbth.gov.gh", "Korle-Bu Teaching Hospital"),
    ("ugmc.gov.gh", "University of Ghana Medical Centre (UGMC)"),
    ("37military.gov.gh", "37 Military Hospital"),
    ("policehospital.gov.gh", "Police Hospital, Accra"),
    ("nyahomedical.com", "Nyaho Medical Centre"),
    ("thetrusthospital.com", "The Trust Hospital"),
    ("accrapsychiatrichospital.org", "Accra Psychiatric Hospital"),
]


def seed_domains(apps, schema_editor):
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")
    for domain, hospital in HOSPITAL_DOMAINS:
        AllowedHospitalDomain.objects.get_or_create(
            domain=domain, defaults={"hospital": hospital}
        )


def unseed_domains(apps, schema_editor):
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")
    AllowedHospitalDomain.objects.filter(
        domain__in=[domain for domain, _ in HOSPITAL_DOMAINS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0004_allowedhospitaldomain_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_domains, unseed_domains),
    ]