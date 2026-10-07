from django.db import migrations

# ---------------------------------------------------------------------------
# Refinement of the hospital email domains seeded by 0007.
#
# Rule applied here: a hospital gets its OWN real domain only when that domain
# actually accepts mail (i.e. a public MX record exists), so the nurse's OTP
# is genuinely deliverable. Where a hospital's branded website has no MX, or
# where the district/regional facility runs on the shared government address,
# the row stays on ghs.gov.gh -- the real mailbox its staff actually use.
# Each domain below was verified with a DNS MX lookup.
# ---------------------------------------------------------------------------

# Clinics whose real, mail-capable domain replaces the shared/default domain.
REAL_DOMAINS = [
    ("Eastern Regional Hospital", "Koforidua", "erhk.org"),
    ("37 Military Hospital", "Burma Camp, Accra", "37milhosp.gov.gh"),
    ("Cape Coast Teaching Hospital", "Cape Coast", "ccthghana.org"),
    ("Tamale Teaching Hospital", "Tamale", "tth.gov.gh"),
    ("Our Lady of Grace Hospital", "Brenu Akyinim, Cape Coast", "olg-hospital.org", "Breman Asikuma, Asikuma/Odoben/Brakwa"),
    ("Agogo Presbyterian Hospital", "Agogo, Asante Akim", "agogopresbyhospital.org"),
    ("Baptist Medical Centre", "Nalerigu, East Mamprusi", "baptistmedicalcenter.org"),
    ("Ho Teaching Hospital", "Ho", "hth.gov.gh"),
]

# Clinics seeded in 0007 with a branded domain that has NO public MX record
# (mail sent there would bounce with 550). Reset them to the shared address.
NO_MX_RESET_TO_GHS = [
    ("University of Ghana Medical Centre", "Legon, Accra"),
    ("St John's Hospital & Fertility Centre", "Tantra Hill, Accra"),
    ("Bemuah Royal Hospital", "East Legon, Accra"),
    ("The Community Hospital", "Ashongman, Accra"),
    ("Saint Martin de Porres Hospital", "Eikwe, Nzema East"),
    ("Saboba Medical Centre", "Saboba"),
    ("Richard Novati Catholic Hospital", "Sogakope, South Tongu"),
    ("West End Hospital", "Kumasi"),
    ("Wesley Clinic", "Kasoa, Awutu Senya East"),
    ("Catholic Hospital", "Apam, Gomoa West"),
    ("Airport Women's Hospital", "Airport Residential Area, Accra"),
    ("Crown Medical Centre", "Adenta West, Accra"),
    ("Del International Hospital", "East Legon, Accra"),
    ("Asafo-Boakye Specialist Hospital", "Ahenema Kokoben, Kumasi"),
    ("SDA Hospital - Wiamoase", "Wiamoase, Sekyere South"),
]

# Allowlist domains added by 0007 that have no MX (bounce risk) - drop them.
DROP_DOMAINS = {
    "ugmc.edu.gh", "tamaleteachinghospital.org", "stjohnsgh.com",
    "bemuahhospital.com", "thecommunityhospitals.org", "eikwe-hospital.org",
    "sabobamedicalcentre.net", "rnch.org", "westend-hospital.com",
    "wesleyclinicgh.com", "apamhospital.com", "airportwomenshospital.com.gh",
    "crownmedgh.com", "delinternationalhospital.org",
    "asafoboakyehospital.com", "sdahospitalwiamoasegh.com",
}

# Newly verified, mail-capable domains to allow.
ADD_DOMAINS = [
    "erhk.org", "37milhosp.gov.gh", "ccthghana.org", "ccth.gov.gh",
    "tth.gov.gh", "olg-hospital.org", "agogopresbyhospital.org",
    "baptistmedicalcenter.org", "hth.gov.gh",
]


def apply(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")

    Clinic.objects.filter(email_domain__in=DROP_DOMAINS).update(email_domain="ghs.gov.gh")

    # Rename the Volta Regional row to its current official name first so the
    # domain mapping below can find it.
    Clinic.objects.filter(name="Volta Regional Hospital", address="Ho").update(
        name="Ho Teaching Hospital"
    )

    for entry in REAL_DOMAINS:
        name, address, domain = entry[0], entry[1], entry[2]
        Clinic.objects.filter(name=name, address=address).update(email_domain=domain)

    Clinic.objects.filter(
        name="Our Lady of Grace Hospital", address="Brenu Akyinim, Cape Coast"
    ).update(address="Breman Asikuma, Asikuma/Odoben/Brakwa")

    AllowedHospitalDomain.objects.filter(domain__in=DROP_DOMAINS).delete()
    for domain in ADD_DOMAINS:
        AllowedHospitalDomain.objects.get_or_create(domain=domain)


def revert(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")

    for domain in DROP_DOMAINS:
        AllowedHospitalDomain.objects.get_or_create(domain=domain)
    AllowedHospitalDomain.objects.filter(domain__in=ADD_DOMAINS).delete()

    # Undo the rename/address fixes.
    Clinic.objects.filter(name="Ho Teaching Hospital", address="Ho").update(
        name="Volta Regional Hospital"
    )
    Clinic.objects.filter(
        name="Our Lady of Grace Hospital", address="Breman Asikuma, Asikuma/Odoben/Brakwa"
    ).update(address="Brenu Akyinim, Cape Coast")

    # Restore the shared domain on everything branded in this migration;
    # the previous state was either ghs.gov.gh or the 0007 branded value.
    for name, address in NO_MX_RESET_TO_GHS:
        Clinic.objects.filter(name=name, address=address).update(email_domain="ghs.gov.gh")


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0008_alter_clinic_options"),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]