from django.db import migrations

# Real hospitals across all 16 regions of Ghana (teaching, regional, municipal,
# district and major mission/private facilities). Address = town/district.
# Phone numbers are intentionally blank rather than fabricated.
HOSPITALS = [
    # --- Greater Accra ---
    ("Korle-Bu Teaching Hospital", "Guggisberg Avenue, Korle Bu, Accra"),
    ("37 Military Hospital", "Burma Camp, Accra"),
    ("Police Hospital", "Cantonments, Accra"),
    ("University of Ghana Medical Centre", "Legon, Accra"),
    ("Greater Accra Regional Hospital (Ridge)", "Castle Road, Adabraka, Accra"),
    ("Princess Marie Louise Children's Hospital", "Dzorwulu, Accra"),
    ("Tema General Hospital", "Community 11, Tema"),
    ("Lekma General Hospital", "Teshie-Nungua, Accra"),
    ("La General Hospital", "La, Accra"),
    ("Achimota Hospital", "Achimota, Accra"),
    ("Accra Psychiatric Hospital", "Accra"),
    ("Pantang Hospital", "Pantang, Accra"),
    ("Adabraka Polyclinic", "Adabraka, Accra"),
    ("Mamprobi Polyclinic", "Mamprobi, Accra"),
    ("Kaneshie Polyclinic", "Kaneshie, Accra"),
    ("Dansoman Polyclinic", "Dansoman, Accra"),
    ("Amasaman District Hospital", "Amasaman"),
    ("Shai Osudoku District Hospital", "Dodowa"),
    ("Weija-Gbawe Municipal Hospital", "Weija"),
    ("Ada East District Hospital", "Ada Foah"),
    ("Ashaiman Polyclinic", "Ashaiman"),
    ("Nyaho Medical Centre", "Airport Residential Area, Accra"),
    ("The Trust Hospital", "Osu, Accra"),

    # --- Eastern ---
    ("Eastern Regional Hospital", "Koforidua"),
    ("St. Joseph's Hospital", "Effiduase, Koforidua"),
    ("Nsawam Government Hospital", "Nsawam"),
    ("Suhum Government Hospital", "Suhum"),
    ("Akosombo General Hospital", "Akosombo"),
    ("Begoro Government Hospital", "Begoro, Fanteakwa"),
    ("Kibi Government Hospital", "Kyebi"),
    ("Oda Government Hospital", "Akyem Oda"),
    ("Kade Government Hospital", "Kade, Kwaebibirem"),
    ("Holy Family Hospital", "Nkawkaw"),
    ("Kwahu Government Hospital", "Atibie, Kwahu South"),
    ("Presbyterian Hospital", "Donkorkrom, Kwahu North"),
    ("St. Dominic's Hospital", "Akwatia, Kwaebibirem"),
    ("St. Martins Hospital", "Agormanya, Lower Manya Krobo"),
    ("Tetteh Quarshie Memorial Hospital", "Akuapim-Mampong"),
    ("Atua Government Hospital", "Odumase-Krobo, Lower Manya Krobo"),
    ("Akuse Government Hospital", "Akuse, Lower Manya Krobo"),
    ("Akim Swedru Government Hospital", "Akim Swedru, Birim South"),

    # --- Central ---
    ("Central Regional Hospital", "Cape Coast"),
    ("Cape Coast Teaching Hospital", "Cape Coast"),
    ("Winneba Government Hospital", "Winneba, Effutu"),
    ("Agona Swedru Government Hospital", "Agona Swedru, Agona West"),
    ("Saltpond Government Hospital", "Saltpond, Mfantsiman"),
    ("Dunkwa Government Hospital", "Dunkwa-on-Offin, Upper Denkyira"),
    ("St. Francis Xavier Hospital", "Assin Foso"),
    ("Ankaful Leprosy/General Hospital", "Ankaful, Cape Coast"),
    ("Ankaful Psychiatric Hospital", "Ankaful, Cape Coast"),
    ("Mother and Child Hospital", "Kasoa, Awutu Senya East"),
    ("Catholic Hospital", "Apam, Gomoa West"),
    ("Our Lady of Grace Hospital", "Brenu Akyinim, Cape Coast"),
    ("Twifo Praso District Hospital", "Twifo Praso"),

    # --- Ashanti ---
    ("Komfo Anokye Teaching Hospital", "Bantama, Kumasi"),
    ("Manhyia District Hospital", "Manhyia, Kumasi"),
    ("Kumasi South Hospital", "Kumasi"),
    ("Suntreso Government Hospital", "Kumasi"),
    ("Agogo Presbyterian Hospital", "Agogo, Asante Akim"),
    ("SDA Hospital", "Asamang, Asante Akim"),
    ("Mampong District Hospital", "Mampong-Ashanti"),
    ("Bekwai District Hospital", "Bekwai"),
    ("Konongo Government Hospital", "Konongo-Odumase"),
    ("Tepa Government Hospital", "Tepa, Ahafo Ano North"),
    ("Jacobu Government Hospital", "Jacobu, Amansie Central"),
    ("Agona Government Hospital", "Agona, Sekyere South"),
    ("Asonomaso Government Hospital", "Asonomaso, Kwabre East"),
    ("Ejura District Hospital", "Ejura"),

    # --- Western ---
    ("Effia Nkwanta Regional Hospital", "Takoradi"),
    ("Essikado Government Hospital", "Takoradi"),
    ("Tarkwa Government Hospital", "Tarkwa, Tarkwa-Nsuaem"),
    ("Bibiani Government Hospital", "Bibiani"),
    ("Saint Martin de Porres Hospital", "Eikwe, Nzema East"),
    ("Nagel Memorial Hospital", "Takoradi"),
    ("Nana Hima Dekyi Hospital", "Dixcove, Ahanta West"),

    # --- Western North ---
    ("St. John of God Hospital", "Sefwi Wiawso"),
    ("Wiawso Government Hospital", "Sefwi Wiawso"),
    ("Enchi Government Hospital", "Enchi, Aowin-Suaman"),
    ("Rooney Memorial Hospital", "Asankragwa, Wassa Amenfi West"),

    # --- Volta ---
    ("Ho Municipal Hospital", "Ho"),
    ("Hohoe District Hospital", "Hohoe"),
    ("Keta District Hospital", "Keta"),
    ("Ketu South Municipal Hospital", "Aflao"),
    ("Peki Government Hospital", "Peki, South Dayi"),
    ("Adidome Government Hospital", "Adidome, North Tongu"),
    ("Sogakope Government Hospital", "Sogakope, South Tongu"),
    ("Margret Marquart Catholic Hospital", "Kpando"),
    ("Anfoega Catholic Hospital", "Anfoega, Kpando"),
    ("St. Anthony's Hospital", "Dzodze, Ketu North"),
    ("Sacred Heart Hospital", "Weme, Abor, Keta"),
    ("Aveyime-Battor Catholic Hospital", "Battor, North Tongu"),

    # --- Oti ---
    ("Nkwanta District Hospital", "Nkwanta"),
    ("Jasikan District Hospital", "Jasikan"),
    ("EP Church Hospital", "Worawora, Jasikan"),
    ("Kete Krachi Government Hospital", "Kete Krachi"),
    ("Mary Theresa Hospital", "Dodi Papase, Kadjebi"),

    # --- Bono ---
    ("Sunyani Regional Hospital", "Sunyani"),
    ("Holy Family Hospital", "Berekum"),
    ("Dormaa Presbyterian Hospital", "Dormaa Ahenkro"),
    ("Sampa Government Hospital", "Sampa, Jaman North"),

    # --- Bono East ---
    ("Holy Family Teaching Hospital", "Techiman"),
    ("Wenchi Methodist Hospital", "Wenchi"),
    ("Nkoranza District Hospital", "Nkoranza"),
    ("Atebubu Government Hospital", "Atebubu"),
    ("Kintampo Municipal Hospital", "Kintampo"),

    # --- Ahafo ---
    ("Goaso Municipal Hospital", "Goaso, Asunafo North"),
    ("Acherensua Government Hospital", "Acherensua, Asutifi"),
    ("St. Elizabeth Hospital", "Hwidiem, Asutifi South"),
    ("St. John of God Hospital", "Duayaw Nkwanta, Tano North"),
    ("Bomaa District Hospital", "Bomaa, Tano North"),
    ("Ahmadiyya Muslim Hospital", "Mim, Asunafo North"),
    ("Bechem Government Hospital", "Bechem, Tano South"),
    ("Banhart Hospital", "Kenyasi, Asutifi North"),

    # --- Northern ---
    ("Tamale Teaching Hospital", "Tamale"),
    ("Tamale West Hospital", "Tamale"),
    ("Yendi District Hospital", "Yendi"),
    ("Bimbilla District Hospital", "Bimbilla, Nanumba North"),
    ("Gushegu District Hospital", "Gushegu"),
    ("Savelugu Municipal Hospital", "Savelugu"),

    # --- Savannah ---
    ("Damongo Government Hospital", "Damongo"),
    ("East Gonja District Hospital", "Salaga"),
    ("Bole District Hospital", "Bole"),

    # --- North East ---
    ("Walewale Government Hospital", "Walewale"),
    ("Baptist Medical Centre", "Nalerigu, East Mamprusi"),

    # --- Upper East ---
    ("Bolgatanga Regional Hospital", "Bolgatanga"),
    ("Navrongo War Memorial Hospital", "Navrongo, Kassena-Nankana"),
    ("Bawku Presbyterian Hospital", "Bawku"),
    ("Zebilla Government Hospital", "Zebilla, Bawku West"),
    ("Sandema District Hospital", "Sandema, Builsa North"),

    # --- Upper West ---
    ("Upper West Regional Hospital", "Wa"),
    ("Lawra District Hospital", "Lawra"),
    ("Nandom Municipal Hospital", "Nandom"),
    ("Jirapa Municipal Hospital", "Jirapa"),
]


def seed_hospitals(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    # Legacy name used by the old bootstrap seed; unify it so two rows never
    # exist for the same hospital.
    Clinic.objects.filter(name="Ridge Hospital").update(
        name="Greater Accra Regional Hospital (Ridge)"
    )
    for name, address in HOSPITALS:
        # Look up on (name, address): some distinct hospitals share a name
        # (e.g. two "St. John of God Hospital" facilities in different towns).
        Clinic.objects.get_or_create(
            name=name,
            address=address,
            defaults={"phone_number": ""},
        )


def unseed_hospitals(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    unify_hospitals = [
        "Greater Accra Regional Hospital (Ridge)",
        "Ridge Hospital",
    ]
    Clinic.objects.filter(
        name__in=[name for name, _ in HOSPITALS] + unify_hospitals
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0005_seed_hospital_email_domains"),
    ]

    operations = [
        migrations.RunPython(seed_hospitals, unseed_hospitals),
    ]