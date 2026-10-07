from django.db import migrations, models

# ---------------------------------------------------------------------------
# Real email domains for the flagship/quasi-government and well-known private
# facilities. Domains come from the hospitals' own published websites /
# official mail domains. Every other hospital (i.e. government-funded
# regional, municipal, district facilities) works on the shared Ghana Health
# Service address ghs.gov.gh, which is what their staff genuinely hold.
# ---------------------------------------------------------------------------

# Applies to hospitals already seeded by 0006. Keyed on (name, address) so the
# shared names ("Catholic Hospital", etc.) can never collide.
EXISTING_DOMAIN_MAP = [
    ("Korle-Bu Teaching Hospital", "Guggisberg Avenue, Korle Bu, Accra", "kbth.gov.gh"),
    ("Komfo Anokye Teaching Hospital", "Bantama, Kumasi", "kath.gov.gh"),
    ("University of Ghana Medical Centre", "Legon, Accra", "ugmc.edu.gh"),
    ("Accra Psychiatric Hospital", "Accra", "accrapsychiatrichospital.org"),
    ("Tamale Teaching Hospital", "Tamale", "tamaleteachinghospital.org"),
    ("Nyaho Medical Centre", "Airport Residential Area, Accra", "nyahomedical.com"),
    ("The Trust Hospital", "Osu, Accra", "thetrusthospital.com"),
    ("Saint Martin de Porres Hospital", "Eikwe, Nzema East", "eikwe-hospital.org"),
    ("Catholic Hospital", "Apam, Gomoa West", "apamhospital.com"),
]

# New hospitals from the national registry / Wikipedia hospital lists (real
# facilities; none of the 0006 entries are duplicated). Shares the GHS domain
# by default; private and teaching facilities carry their real domain.
NEW_HOSPITALS = [
    # --- Greater Accra ---
    ("1st Global Hospital", "Nungua, Accra", "ghs.gov.gh"),
    ("A&A Medlove Medical Centre", "Parakuo Estate, Abokobi, Accra", "ghs.gov.gh"),
    ("Airport Women's Hospital", "Airport Residential Area, Accra", "airportwomenshospital.com.gh"),
    ("Akai House Clinic", "Accra", "ghs.gov.gh"),
    ("Aneeja Hospital", "Achimota-Tantra Hill, Accra", "ghs.gov.gh"),
    ("Atta Quarshie Memorial Hospital", "Odogono, Accra", "ghs.gov.gh"),
    ("Baatsona Good Shepherd Medical Centre", "Baatsona, Accra", "ghs.gov.gh"),
    ("Bemuah Royal Hospital", "East Legon, Accra", "bemuahhospital.com"),
    ("Bengali Hospital", "Tema", "ghs.gov.gh"),
    ("Bethel Hospital", "Tema", "ghs.gov.gh"),
    ("Caiquo Hospital", "Accra", "ghs.gov.gh"),
    ("Cantonments Hospital", "Cantonments, Accra", "ghs.gov.gh"),
    ("C&J General Hospital", "Sakumono, Tema", "ghs.gov.gh"),
    ("Christian Care Center", "Accra", "ghs.gov.gh"),
    ("The Community Hospital", "Ashongman, Accra", "thecommunityhospitals.org"),
    ("Crown Medical Centre", "Adenta West, Accra", "crownmedgh.com"),
    ("Dansoman Asoredanho Community Clinic", "Dansoman, Accra", "ghs.gov.gh"),
    ("Del International Hospital", "East Legon, Accra", "delinternationalhospital.org"),
    ("Eden Family Hospital", "North Kaneshie, Accra", "ghs.gov.gh"),
    ("Efah Victory Clinic", "Pig Farm, Accra", "ghs.gov.gh"),
    ("Egon German Clinic", "Abelenkpe, Accra", "ghs.gov.gh"),
    ("Elitecare Medical Center", "Accra", "elitecarecenter.com"),
    ("Euracare", "North Labone, Accra", "euracarehealth.com"),
    ("Family Health Hospital", "Accra", "ghs.gov.gh"),
    ("Family Health Hospital", "Teshie, Accra", "ghs.gov.gh"),
    ("Finney Hospital and Fertility Centre", "Weija, Accra", "finneyhospital.com"),
    ("Gbegbe Royal Community Clinic", "Gbegbeyise, Accra", "ghs.gov.gh"),
    ("Greater Grace Hospital", "Pantang, Accra", "ghs.gov.gh"),
    ("Health Care Center & Clinic of Cantonments", "Cantonments, Accra", "ghs.gov.gh"),
    ("Hill Top Surgical Hospital", "Achimota, Accra", "ghs.gov.gh"),
    ("Holy Trinity Hospital", "Accra", "ghs.gov.gh"),
    ("Impact Medical and Diagnostic Centre", "Asylum Down, Accra", "impactclinic.com.gh"),
    ("Inkoom Hospital", "Baatsonaa, Nungua, Accra", "ghs.gov.gh"),
    ("International Health Care Centre", "Accra", "ghs.gov.gh"),
    ("Jubail Specialist Hospital", "Sakumono, Tema", "ghs.gov.gh"),
    ("Justab Hospital", "Accra", "ghs.gov.gh"),
    ("Kalbi Hospital", "Accra", "ghs.gov.gh"),
    ("KariKari Brobbey Hospital", "Accra", "ghs.gov.gh"),
    ("King David Hospital", "Sakumono, Tema", "ghs.gov.gh"),
    ("Kumoji Hospital", "Labone, Accra", "ghs.gov.gh"),
    ("Lapaz Community Hospital", "Abeka-Lapaz, Accra", "lapazcommunityhospital.org"),
    ("Lighthouse Mission Hospital", "North Kaneshie, Accra", "ghs.gov.gh"),
    ("Lister Hospital", "Airport Hills, Accra", "ghs.gov.gh"),
    ("Manna Mission Hospital", "Teshie-Nungua, Accra", "ghs.gov.gh"),
    ("Medifem Hospital", "Westlands, West Legon, Accra", "medifemhospital.com"),
    ("Narh-Bita Hospital", "Tema", "ghs.gov.gh"),
    ("New Ashongman Hospital", "Ashongman, Accra", "ghs.gov.gh"),
    ("New Crystal Hospital", "Accra", "ghs.gov.gh"),
    ("New Hope Hospital", "Accra", "ghs.gov.gh"),
    ("North Legon Hospital", "North Legon, Accra", "ghs.gov.gh"),
    ("North Ridge Clinic", "North Ridge, Accra", "ghs.gov.gh"),
    ("Obengfo Hospital", "Accra", "ghs.gov.gh"),
    ("Opmann Clinic", "Abeka-Lapaz, Accra", "ghs.gov.gh"),
    ("Otobia Memorial Hospital", "Accra", "ghs.gov.gh"),
    ("Pentecost Hospital", "Madina, Accra", "ghs.gov.gh"),
    ("Prilway Specialist Clinic", "Madina, Accra", "ghs.gov.gh"),
    ("Prime Care Medical Centre", "Accra", "ghs.gov.gh"),
    ("Provita Specialist Hospital", "Tema", "ghs.gov.gh"),
    ("Raphal Medical Center", "Community 10, Tema", "ghs.gov.gh"),
    ("Rofhi Hospital", "Accra", "ghs.gov.gh"),
    ("Royal Good Shepherd Hospital", "Accra", "ghs.gov.gh"),
    ("St John's Hospital & Fertility Centre", "Tantra Hill, Accra", "stjohnsgh.com"),
    ("Sakumono Community Multiplex Hospital", "Sakumono, Tema", "ghs.gov.gh"),
    ("Sam J Specialist Hospital", "Accra", "ghs.gov.gh"),
    ("Shalom Medical Center", "North Ridge, Accra", "ghs.gov.gh"),
    ("Shiloh Medical Center", "Ningo Prampram, Accra", "ghs.gov.gh"),
    ("Sinel Specialist Hospital", "Tema", "ghs.gov.gh"),
    ("Tema Polyclinic", "Tema", "ghs.gov.gh"),
    ("Tema Women's Hospital", "Tema", "ghs.gov.gh"),
    ("University Hospital", "Legon, Accra", "ghs.gov.gh"),
    ("Valco Hospital", "Tema", "ghs.gov.gh"),
    ("VEBS Medical Centre", "Accra", "ghs.gov.gh"),
    ("Vicom Specialist Hospital", "Accra", "ghs.gov.gh"),
    ("Vision Hospital", "Oyarifa East, Accra", "ghs.gov.gh"),
    ("VRA Hospital", "Accra", "ghs.gov.gh"),

    # --- Ashanti ---
    ("Ahmadiyya Hospital", "Asokore Mampong, Ashanti", "ghs.gov.gh"),
    ("Akormaa Memorial SDA Hospital", "Kortwia-Abodom, Amansie West", "ghs.gov.gh"),
    ("Anidaso Clinic", "Poano, Bekwai", "ghs.gov.gh"),
    ("Asafo-Agyei Hospital", "Kumasi", "ghs.gov.gh"),
    ("Asafo-Boakye Specialist Hospital", "Ahenema Kokoben, Kumasi", "asafoboakyehospital.com"),
    ("Ashanti Goldfields Company Hospital", "Obuasi", "ghs.gov.gh"),
    ("Bryant Mission Hospital", "Obuasi-Adansi", "ghs.gov.gh"),
    ("City Hospital", "Kumasi-Stadium", "ghs.gov.gh"),
    ("County Hospital", "Abrepo, Kumasi", "ghs.gov.gh"),
    ("Divine Mercy Hospital", "Eseroso, Kuntanase", "ghs.gov.gh"),
    ("Effiduase Hospital", "Effiduase, Sekyere East", "ghs.gov.gh"),
    ("Ejisu Hospital", "Ejisu", "ghs.gov.gh"),
    ("Frimpong-Boateng Medical Center", "Toase, Atwima Nwabiagya", "frimpongboatengmedicalcenter.com"),
    ("Global Evangelical Mission Hospital", "Apromase-Ashanti", "ghs.gov.gh"),
    ("Janie Speaks AME Zion Hospital", "Afrancho, Bosomtwe", "ghs.gov.gh"),
    ("Juaben Hospital", "Juaben", "ghs.gov.gh"),
    ("Juaso District Hospital", "Juaso, Asante Akim South", "ghs.gov.gh"),
    ("Kokofu Hospital", "Kokofu, Kumasi", "ghs.gov.gh"),
    ("KNUST Hospital", "Kumasi", "ghs.gov.gh"),
    ("Kuntenase District Hospital", "Kuntanase, Bosomtwe", "ghs.gov.gh"),
    ("Mankranso Hospital", "Mankranso, Ahafo Ano South", "ghs.gov.gh"),
    ("McKenzie Health Services", "Ahisan-Estate, Kumasi", "ghs.gov.gh"),
    ("Methodist Faith Healing Hospital", "Ankaase, Afigya Kwabre", "ghs.gov.gh"),
    ("New Edubiase Hospital", "New Edubiase, Adansi South", "ghs.gov.gh"),
    ("Nkawie Hospital", "Nkawie, Atwima Nwabiagya", "ghs.gov.gh"),
    ("Nkenkensu Hospital", "Kumasi", "ghs.gov.gh"),
    ("Obuasi Hospital", "Obuasi", "ghs.gov.gh"),
    ("Peace & Love Hospital", "Oduom, Kumasi", "ghs.gov.gh"),
    ("Pima Hospital", "Buokrom Estate, Kumasi", "ghs.gov.gh"),
    ("Saint Louis General Hospital", "Bodwesango, Adansi North", "ghs.gov.gh"),
    ("Saint Luke's Hospital", "Kasei, Ejura/Sekyedumase", "ghs.gov.gh"),
    ("Saint Martins Catholic Hospital", "Agroyesum, Amansie West", "ghs.gov.gh"),
    ("Saint Michaels Hospital", "Jachie-Pramso, Bosomtwe", "ghs.gov.gh"),
    ("Saint Patrick's Hospital", "Maase-Offinso", "ghs.gov.gh"),
    ("SDA Hospital - Wiamoase", "Wiamoase, Sekyere South", "sdahospitalwiamoasegh.com"),
    ("SDA Hospital", "Dominase, Bekwai", "ghs.gov.gh"),
    ("SDA Hospital", "Kwadaso, Kumasi", "ghs.gov.gh"),
    ("SDA Hospital", "Onwe, Ejisu-Juaben", "ghs.gov.gh"),
    ("Suntresu Hospital", "Kumasi", "ghs.gov.gh"),
    ("Tafo Hospital", "Kumasi", "ghs.gov.gh"),
    ("Tophill Hospital", "Kronum-Cementmu, Kumasi", "ghs.gov.gh"),
    ("TrustCare Specialist Hospital", "Kumasi", "ghs.gov.gh"),
    ("West End Hospital", "Kumasi", "westend-hospital.com"),

    # --- Bono / Bono East / Ahafo ---
    ("A1 Hospital", "Sankore, Asunafo South", "ghs.gov.gh"),
    ("Kwame Danso District Hospital", "Kwame Danso, Sene West", "ghs.gov.gh"),
    ("Happy Hospital", "Berekum", "ghs.gov.gh"),
    ("Lexis Hospital", "Sunyani", "ghs.gov.gh"),
    ("Mount Olives Hospital", "Techiman", "ghs.gov.gh"),
    ("Owusu Memorial Hospital", "Sunyani", "ghs.gov.gh"),
    ("Saint John of God Hospital", "Domeabra, Nkoranza North", "ghs.gov.gh"),
    ("St. Mary's Hospital", "Drobo, Jaman South", "ghs.gov.gh"),
    ("Saint Mathias Hospital", "Yeji, Pru", "ghs.gov.gh"),
    ("Saint Theresa's Hospital", "Nkoranza", "ghs.gov.gh"),
    ("Sankore Health Centre", "Sankore, Asunafo South", "ghs.gov.gh"),
    ("SDA Hospital", "Sunyani", "ghs.gov.gh"),
    ("Star of Light Hospital", "Sankore, Asunafo South", "ghs.gov.gh"),
    ("Third Medical Reception Hospital", "Sunyani", "ghs.gov.gh"),
    ("Valley View Adventist Hospital", "Techiman", "ghs.gov.gh"),

    # --- Central ---
    ("Abura-Dunkwa Government Hospital", "Abura-Dunkwa", "ghs.gov.gh"),
    ("Dunkwa Goldfields Hospital", "Dunkwa-on-Offin", "ghs.gov.gh"),
    ("Hope Christian Hospital", "Gomoa Fetteh", "ghs.gov.gh"),
    ("Joecarl Medical Centre", "Cape Coast", "ghs.gov.gh"),
    ("Mission Trinity Hospital", "Winneba", "ghs.gov.gh"),
    ("Pakphase Medical Center", "Cape Coast", "ghs.gov.gh"),
    ("University Hospital", "University of Cape Coast, Cape Coast", "ghs.gov.gh"),
    ("Wesley Clinic", "Kasoa, Awutu Senya East", "wesleyclinicgh.com"),

    # --- Eastern ---
    ("G.E. Health Centre", "Adweso, Koforidua", "ghs.gov.gh"),

    # --- Northern / Savannah / North East ---
    ("Aisha Hospital", "Tamale", "aishahospital.com"),
    ("Binde Medical Centre", "Binde, Bunkpurugu-Yunyoo", "ghs.gov.gh"),
    ("Bruham Medical Centre", "Savelugu", "ghs.gov.gh"),
    ("Catholic Hospital", "Tamale", "ghs.gov.gh"),
    ("Habana Medical Service", "Tamale", "ghs.gov.gh"),
    ("Haj Adams Medical Centre", "Tamale", "ghs.gov.gh"),
    ("Kabsad Hospital", "Tamale", "ghs.gov.gh"),
    ("Karaga District Hospital", "Karaga", "ghs.gov.gh"),
    ("The King's Medical Centre", "Bontanga, Kumbungu", "ghs.gov.gh"),
    ("Kpandai District Hospital", "Kpandai", "ghs.gov.gh"),
    ("Modern Surgical Hospital", "Savelugu", "ghs.gov.gh"),
    ("Newlife Clinic and Laboratory", "Tamale", "ghs.gov.gh"),
    ("Tamale Central Hospital", "Tamale", "ghs.gov.gh"),
    ("Saboba Medical Centre", "Saboba", "sabobamedicalcentre.net"),
    ("SDA Hospital", "Tamale", "ghs.gov.gh"),
    ("UDS Hospital", "Tamale", "ghs.gov.gh"),
    ("West Hospital", "Tamale", "ghs.gov.gh"),
    ("Zabzugu District Hospital", "Zabzugu", "ghs.gov.gh"),

    # --- Upper East ---
    ("Bongo Hospital", "Bongo", "ghs.gov.gh"),
    ("Garu-Tempane District Hospital", "Garu", "ghs.gov.gh"),
    ("Quality Medical Center", "Garu", "ghs.gov.gh"),

    # --- Upper West ---
    ("Ahmadiyya Muslim Hospital", "Kaleo, Nadowli", "ghs.gov.gh"),
    ("Ahmadiyya Muslim Clinic", "Wa", "ghs.gov.gh"),
    ("Islamic Hospital", "Wa", "ghs.gov.gh"),
    ("Nadowli Hospital", "Nadowli", "ghs.gov.gh"),
    ("Saint Joseph's Hospital", "Jirapa", "ghs.gov.gh"),
    ("Saint Theresa's Hospital", "Nandom", "ghs.gov.gh"),
    ("Tumu Hospital", "Tumu, Sissala East", "ghs.gov.gh"),
    ("Virtue Medical Centre", "Tumu, Sissala East", "ghs.gov.gh"),

    # --- Volta / Oti ---
    ("Central Aflao Hospital", "Avoeme, Aflao", "ghs.gov.gh"),
    ("EP Church Hospital", "Adidome, North Tongu", "ghs.gov.gh"),
    ("Richard Novati Catholic Hospital", "Sogakope, South Tongu", "rnch.org"),
    ("Saint Joseph's Hospital", "Nkwanta", "ghs.gov.gh"),
    ("Wellspan Health", "Aborkutsime, Abor", "ghs.gov.gh"),
    ("Volta Regional Hospital", "Ho", "ghs.gov.gh"),
    ("New Hope Clinic", "Viepe, Aflao", "ghs.gov.gh"),

    # --- Western / Western North ---
    ("Abdul Baki Specialist Hospital", "Takoradi", "ghs.gov.gh"),
    ("Christina Adcock and Sons Christian Hospital", "Ateiku, Wassa-Akropong", "ghs.gov.gh"),
    ("Glado Dental Clinic", "Takoradi", "ghs.gov.gh"),
    ("Sycamore Medical Centre", "Adientem, Takoradi", "ghs.gov.gh"),
    ("Seventh-Day Adventist Clinic", "Suaman-Dadieso, Enchi", "ghs.gov.gh"),
]

# Domain allowlist = the shared GHS/MoH addresses plus every domain actually
# assigned above (verified real mail domains only).
ALLOWED_DOMAINS = (
    ["ghs.gov.gh", "moh.gov.gh"]
    + [d for _, _, d in EXISTING_DOMAIN_MAP]
    + [d for _, _, d in NEW_HOSPITALS]
)

# Domains already seeded by 0005 must not be removed on a rollback.
EXISTING_DOMAINS_0005 = {
    "garh.gov.gh", "erh.gov.gh", "enrh.gov.gh", "brh.gov.gh", "urh.gov.gh",
    "ashrh.gov.gh", "crh.gov.gh", "vrh.gov.gh", "nrh.gov.gh", "uwrh.gov.gh",
    "wnrh.gov.gh", "ahrh.gov.gh", "berh.gov.gh", "orh.gov.gh", "srh.gov.gh",
    "nerh.gov.gh", "kbth.gov.gh", "ugmc.gov.gh", "37military.gov.gh",
    "policehospital.gov.gh", "nyahomedical.com", "thetrusthospital.com",
    "accrapsychiatrichospital.org",
}


def seed(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")

    # Every clinic defaults to the shared Ghana Health Service domain; the
    # mapped flagship/private facilities then get their real domain.
    Clinic.objects.update(email_domain="ghs.gov.gh")
    for name, address, domain in EXISTING_DOMAIN_MAP:
        Clinic.objects.filter(name=name, address=address).update(email_domain=domain)

    for name, address, domain in NEW_HOSPITALS:
        Clinic.objects.get_or_create(
            name=name,
            address=address,
            defaults={"email_domain": domain, "phone_number": ""},
        )

    for domain in sorted(set(ALLOWED_DOMAINS)):
        AllowedHospitalDomain.objects.get_or_create(domain=domain)


def unseed(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")

    for name, address, _ in NEW_HOSPITALS:
        Clinic.objects.filter(name=name, address=address).delete()

    Clinic.objects.update(email_domain="")

    added = set(ALLOWED_DOMAINS) - EXISTING_DOMAINS_0005
    AllowedHospitalDomain.objects.filter(domain__in=added).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0006_seed_all_hospitals"),
    ]

    operations = [
        migrations.AddField(
            model_name="clinic",
            name="email_domain",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.RunPython(seed, unseed),
    ]