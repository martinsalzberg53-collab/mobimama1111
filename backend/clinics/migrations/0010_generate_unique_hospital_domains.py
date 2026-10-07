from django.db import migrations
from django.utils.text import slugify

# ---------------------------------------------------------------------------
# Give every hospital its own unique email domain, real-internet style.
#
# The 22 hospitals that genuinely run their own mail keep their verified
# domain (kbth.gov.gh, hth.gov.gh, olg-hospital.org, ...). Every remaining
# hospital gets a deterministic, unique domain derived from its name
# (e.g. "Tema General Hospital" -> tema-general-hospital.gov.gh), following
# the same pattern real Ghanaian public hospitals use (<abbr>.gov.gh).
#
# NOTE: only the verified domains accept real mail. The derived domains are
# for identification on the registration dropdown; registering a nurse with
# one of them will NOT receive a mail-delivered OTP.
# ---------------------------------------------------------------------------

# Real, mail-capable domains already assigned - never overwrite these.
REAL_DOMAINS = {
    "37milhosp.gov.gh", "accrapsychiatrichospital.org", "agogopresbyhospital.org",
    "aishahospital.com", "baptistmedicalcenter.org", "ccthghana.org",
    "elitecarecenter.com", "erhk.org", "euracarehealth.com", "finneyhospital.com",
    "frimpongboatengmedicalcenter.com", "ghs.gov.gh", "hth.gov.gh",
    "impactclinic.com.gh", "kath.gov.gh", "kbth.gov.gh", "lapazcommunityhospital.org",
    "medifemhospital.com", "nyahomedical.com", "olg-hospital.org",
    "thetrusthospital.com", "tth.gov.gh",
}

# Domains that are real but shared/ministry-level, or reserved - never generate
# or overwrite these either.
RESERVED = {"ghs.gov.gh", "moh.gov.gh"}


def _unique_domain(name, address, taken):
    base = slugify(name)[:48] or "hospital"
    candidate = base + ".gov.gh"
    if candidate not in taken:
        taken.add(candidate)
        return candidate
    town = slugify((address or "").split(",")[0])[:20] or base
    candidate = f"{base}-{town}"[:48] + ".gov.gh"
    if candidate not in taken:
        taken.add(candidate)
        return candidate
    n = 2
    while f"{base}-{n}"[:48] + ".gov.gh" in taken:
        n += 1
    candidate = f"{base}-{n}"[:48] + ".gov.gh"
    taken.add(candidate)
    return candidate


def apply(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")

    taken = set(REAL_DOMAINS)
    for row in Clinic.objects.exclude(email_domain="").exclude(email_domain__in=RESERVED).values_list("email_domain", flat=True):
        taken.add(row)

    changed = []
    for clinic in Clinic.objects.filter(email_domain__in=("", "ghs.gov.gh", "moh.gov.gh")).order_by("name", "address"):
        domain = _unique_domain(clinic.name, clinic.address, taken)
        clinic.email_domain = domain
        clinic.save(update_fields=["email_domain"])
        changed.append(domain)

    for domain in changed:
        AllowedHospitalDomain.objects.get_or_create(domain=domain)


def revert(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")

    generated = list(
        Clinic.objects.exclude(email_domain__in=REAL_DOMAINS)
        .exclude(email_domain="")
        .values_list("email_domain", flat=True)
    )
    Clinic.objects.exclude(email_domain__in=REAL_DOMAINS).exclude(email_domain="").update(
        email_domain="ghs.gov.gh"
    )
    AllowedHospitalDomain.objects.filter(domain__in=generated).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0009_seed_refined_hospital_domains"),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]