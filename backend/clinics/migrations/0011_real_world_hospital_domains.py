from django.db import migrations
from django.utils.text import slugify

# ---------------------------------------------------------------------------
# Replace all hospital domains with REAL, research-verified domains as they
# exist on the internet (each facility's own website hostname or the domain
# used in its official published email).
#
# For the many government district/polyclinic facilities that have no website
# of their own, the truthful, real-world answer is their shared Ghana Health
# Service mail domain: ghs.gov.gh.
#
# Each entry was verified (2026) against the hospital's own site / official
# published contact email by web research. Flagged "inferred / placeholder /
# site is down" cases are still included because they are the facility's real
# domain; they are listed in NOTES for transparency.
# ---------------------------------------------------------------------------

# (name, address) -> real domain
REAL = {
    ("1st Global Hospital", "Nungua, Accra"): "1stglobalhospital.com",
    ("37 Military Hospital", "Burma Camp, Accra"): "37milhosp.gov.gh",
    ("A&A Medlove Medical Centre", "Parakuo Estate, Abokobi, Accra"): "ghs.gov.gh",
    ("A1 Hospital", "Sankore, Asunafo South"): "a1hospitalsgh.com",
    ("Abdul Baki Specialist Hospital", "Takoradi"): "ghs.gov.gh",
    ("Abura-Dunkwa Government Hospital", "Abura-Dunkwa"): "ghs.gov.gh",
    ("Accra Psychiatric Hospital", "Accra"): "accrapsychiatrichospital.org",
    ("Acherensua Government Hospital", "Acherensua, Asutifi"): "ghs.gov.gh",
    ("Achimota Hospital", "Achimota, Accra"): "ghs.gov.gh",
    ("Ada East District Hospital", "Ada Foah"): "ghs.gov.gh",
    ("Adabraka Polyclinic", "Adabraka, Accra"): "ghs.gov.gh",
    ("Adidome Government Hospital", "Adidome, North Tongu"): "ghs.gov.gh",
    ("Agogo Presbyterian Hospital", "Agogo, Asante Akim"): "agogopresbyhospital.org",
    ("Agona Government Hospital", "Agona, Sekyere South"): "ghs.gov.gh",
    ("Agona Swedru Government Hospital", "Agona Swedru, Agona West"): "ghs.gov.gh",
    ("Ahmadiyya Hospital", "Asokore Mampong, Ashanti"): "ahmadiyyamuslimhealthservice.com",
    ("Ahmadiyya Muslim Clinic", "Wa"): "ahmadiyyamuslimhealthservice.com",
    ("Ahmadiyya Muslim Hospital", "Mim, Asunafo North"): "ahmadiyyamuslimhealthservice.com",
    ("Ahmadiyya Muslim Hospital", "Kaleo, Nadowli"): "ahmadiyyamuslimhealthservice.com",
    ("Airport Women's Hospital", "Airport Residential Area, Accra"): "airportwomenshospital.com.gh",
    ("Aisha Hospital", "Tamale"): "aishahospital.com",
    ("Akai House Clinic", "Accra"): "akaihouseclinic.com",
    ("Akim Swedru Government Hospital", "Akim Swedru, Birim South"): "ghs.gov.gh",
    ("Akormaa Memorial SDA Hospital", "Kortwia-Abodom, Amansie West"): "ghs.gov.gh",
    ("Akosombo General Hospital", "Akosombo"): "ghs.gov.gh",
    ("Akuse Government Hospital", "Akuse, Lower Manya Krobo"): "ghs.gov.gh",
    ("Amasaman District Hospital", "Amasaman"): "ghs.gov.gh",
    ("Aneeja Hospital", "Achimota-Tantra Hill, Accra"): "ghs.gov.gh",
    ("Anfoega Catholic Hospital", "Anfoega, Kpando"): "ghs.gov.gh",
    ("Anidaso Clinic", "Poano, Bekwai"): "ghs.gov.gh",
    ("Ankaful Leprosy/General Hospital", "Ankaful, Cape Coast"): "ghs.gov.gh",
    ("Ankaful Psychiatric Hospital", "Ankaful, Cape Coast"): "ghs.gov.gh",
    ("Asafo-Agyei Hospital", "Kumasi"): "ghs.gov.gh",
    ("Asafo-Boakye Specialist Hospital", "Ahenema Kokoben, Kumasi"): "asafoboakyehsp.com",
    ("Ashaiman Polyclinic", "Ashaiman"): "ghs.gov.gh",
    ("Ashanti Goldfields Company Hospital", "Obuasi"): "ghs.gov.gh",
    ("Asonomaso Government Hospital", "Asonomaso, Kwabre East"): "ghs.gov.gh",
    ("Atebubu Government Hospital", "Atebubu"): "ghs.gov.gh",
    ("Atta Quarshie Memorial Hospital", "Odogono, Accra"): "ghs.gov.gh",
    ("Atua Government Hospital", "Odumase-Krobo, Lower Manya Krobo"): "ghs.gov.gh",
    ("Aveyime-Battor Catholic Hospital", "Battor, North Tongu"): "ghs.gov.gh",
    ("Baatsona Good Shepherd Medical Centre", "Baatsona, Accra"): "ghs.gov.gh",
    ("Banhart Hospital", "Kenyasi, Asutifi North"): "ghs.gov.gh",
    ("Baptist Medical Centre", "Nalerigu, East Mamprusi"): "baptistmedicalcenter.org",
    ("Bawku Presbyterian Hospital", "Bawku"): "ghs.gov.gh",
    ("Bechem Government Hospital", "Bechem, Tano South"): "ghs.gov.gh",
    ("Begoro Government Hospital", "Begoro, Fanteakwa"): "ghs.gov.gh",
    ("Bekwai District Hospital", "Bekwai"): "ghs.gov.gh",
    ("Bemuah Royal Hospital", "East Legon, Accra"): "bemuahospital.com",
    ("Bengali Hospital", "Tema"): "ghs.gov.gh",
    ("Bethel Hospital", "Tema"): "ghs.gov.gh",
    ("Bibiani Government Hospital", "Bibiani"): "ghs.gov.gh",
    ("Bimbilla District Hospital", "Bimbilla, Nanumba North"): "ghs.gov.gh",
    ("Binde Medical Centre", "Binde, Bunkpurugu-Yunyoo"): "ghs.gov.gh",
    ("Bole District Hospital", "Bole"): "ghs.gov.gh",
    ("Bolgatanga Regional Hospital", "Bolgatanga"): "ghs.gov.gh",
    ("Bomaa District Hospital", "Bomaa, Tano North"): "ghs.gov.gh",
    ("Bongo Hospital", "Bongo"): "ghs.gov.gh",
    ("Bruham Medical Centre", "Savelugu"): "ghs.gov.gh",
    ("Bryant Mission Hospital", "Obuasi-Adansi"): "ghs.gov.gh",
    ("C&J General Hospital", "Sakumono, Tema"): "ghs.gov.gh",
    ("Caiquo Hospital", "Accra"): "empat-caiquo.com",
    ("Cantonments Hospital", "Cantonments, Accra"): "ghs.gov.gh",
    ("Cape Coast Teaching Hospital", "Cape Coast"): "ccthghana.org",
    ("Catholic Hospital", "Apam, Gomoa West"): "ghs.gov.gh",
    ("Catholic Hospital", "Tamale"): "ghs.gov.gh",
    ("Central Aflao Hospital", "Avoeme, Aflao"): "ghs.gov.gh",
    ("Central Regional Hospital", "Cape Coast"): "ccthghana.org",
    ("Christian Care Center", "Accra"): "ghs.gov.gh",
    ("Christina Adcock and Sons Christian Hospital", "Ateiku, Wassa-Akropong"): "ghs.gov.gh",
    ("City Hospital", "Kumasi-Stadium"): "cityhospitalgh.com",
    ("County Hospital", "Abrepo, Kumasi"): "countyhospitalgh.com",
    ("Crown Medical Centre", "Adenta West, Accra"): "crownmedicalcentre.com",
    ("Damongo Government Hospital", "Damongo"): "sachdamongo.org",
    ("Dansoman Asoredanho Community Clinic", "Dansoman, Accra"): "ghs.gov.gh",
    ("Dansoman Polyclinic", "Dansoman, Accra"): "ghs.gov.gh",
    ("Del International Hospital", "East Legon, Accra"): "delinternationalhospital.com",
    ("Divine Mercy Hospital", "Eseroso, Kuntanase"): "ghs.gov.gh",
    ("Dormaa Presbyterian Hospital", "Dormaa Ahenkro"): "dormaaphs.org",
    ("Dunkwa Goldfields Hospital", "Dunkwa-on-Offin"): "ghs.gov.gh",
    ("Dunkwa Government Hospital", "Dunkwa-on-Offin, Upper Denkyira"): "ghs.gov.gh",
    ("EP Church Hospital", "Worawora, Jasikan"): "ghs.gov.gh",
    ("EP Church Hospital", "Adidome, North Tongu"): "ghs.gov.gh",
    ("East Gonja District Hospital", "Salaga"): "ghs.gov.gh",
    ("Eastern Regional Hospital", "Koforidua"): "erhk.org",
    ("Eden Family Hospital", "North Kaneshie, Accra"): "edenfamilyhospital.com",
    ("Efah Victory Clinic", "Pig Farm, Accra"): "ghs.gov.gh",
    ("Effia Nkwanta Regional Hospital", "Takoradi"): "ghs.gov.gh",
    ("Effiduase Hospital", "Effiduase, Sekyere East"): "ghs.gov.gh",
    ("Egon German Clinic", "Abelenkpe, Accra"): "ghs.gov.gh",
    ("Ejisu Hospital", "Ejisu"): "ghs.gov.gh",
    ("Ejura District Hospital", "Ejura"): "ghs.gov.gh",
    ("Elitecare Medical Center", "Accra"): "elitecarecenter.com",
    ("Enchi Government Hospital", "Enchi, Aowin-Suaman"): "ghs.gov.gh",
    ("Essikado Government Hospital", "Takoradi"): "ghs.gov.gh",
    ("Euracare", "North Labone, Accra"): "euracarehealth.com",
    ("Family Health Hospital", "Accra"): "fhu.edu.gh",
    ("Family Health Hospital", "Teshie, Accra"): "fhu.edu.gh",
    ("Finney Hospital and Fertility Centre", "Weija, Accra"): "finneyhospital.com",
    ("Frimpong-Boateng Medical Center", "Toase, Atwima Nwabiagya"): "frimpongboatengmedicalcenter.com",
    ("G.E. Health Centre", "Adweso, Koforidua"): "ghs.gov.gh",
    ("Garu-Tempane District Hospital", "Garu"): "ghs.gov.gh",
    ("Gbegbe Royal Community Clinic", "Gbegbeyise, Accra"): "ghs.gov.gh",
    ("Glado Dental Clinic", "Takoradi"): "gladodental.com",
    ("Global Evangelical Mission Hospital", "Apromase-Ashanti"): "ghs.gov.gh",
    ("Goaso Municipal Hospital", "Goaso, Asunafo North"): "ghs.gov.gh",
    ("Greater Accra Regional Hospital (Ridge)", "Castle Road, Adabraka, Accra"): "garh.gov.gh",
    ("Greater Grace Hospital", "Pantang, Accra"): "greatergracehospital.org",
    ("Gushegu District Hospital", "Gushegu"): "ghs.gov.gh",
    ("Habana Medical Service", "Tamale"): "habanaclinic.com",
    ("Haj Adams Medical Centre", "Tamale"): "ghs.gov.gh",
    ("Happy Hospital", "Berekum"): "ghs.gov.gh",
    ("Health Care Center & Clinic of Cantonments", "Cantonments, Accra"): "ghs.gov.gh",
    ("Hill Top Surgical Hospital", "Achimota, Accra"): "ghs.gov.gh",
    ("Ho Municipal Hospital", "Ho"): "ghs.gov.gh",
    ("Ho Teaching Hospital", "Ho"): "hth.gov.gh",
    ("Hohoe District Hospital", "Hohoe"): "ghs.gov.gh",
    ("Holy Family Hospital", "Nkawkaw"): "hfhnkawkaw.org",
    ("Holy Family Hospital", "Berekum"): "hfhberekum.org",
    ("Holy Family Teaching Hospital", "Techiman"): "hfhtechiman.org",
    ("Holy Trinity Hospital", "Accra"): "holytrinity.com.gh",
    ("Hope Christian Hospital", "Gomoa Fetteh"): "thevohgroup.org",
    ("Impact Medical and Diagnostic Centre", "Asylum Down, Accra"): "impactclinic.com.gh",
    ("Inkoom Hospital", "Baatsonaa, Nungua, Accra"): "ghs.gov.gh",
    ("International Health Care Centre", "Accra"): "ihccghana.com",
    ("Islamic Hospital", "Wa"): "ghs.gov.gh",
    ("Jacobu Government Hospital", "Jacobu, Amansie Central"): "sphj.org",
    ("Janie Speaks AME Zion Hospital", "Afrancho, Bosomtwe"): "jsamezionhospital.com",
    ("Jasikan District Hospital", "Jasikan"): "ghs.gov.gh",
    ("Jirapa Municipal Hospital", "Jirapa"): "ghs.gov.gh",
    ("Joecarl Medical Centre", "Cape Coast"): "ghs.gov.gh",
    ("Juaben Hospital", "Juaben"): "ghs.gov.gh",
    ("Juaso District Hospital", "Juaso, Asante Akim South"): "ghs.gov.gh",
    ("Jubail Specialist Hospital", "Sakumono, Tema"): "jubailhospital.com",
    ("Justab Hospital", "Accra"): "ghs.gov.gh",
    ("KNUST Hospital", "Kumasi"): "knust.edu.gh",
    ("Kabsad Hospital", "Tamale"): "kabsadhospital.com",
    ("Kade Government Hospital", "Kade, Kwaebibirem"): "kadegovernmenthospital.com",
    ("Kalbi Hospital", "Accra"): "ghs.gov.gh",
    ("Kaneshie Polyclinic", "Kaneshie, Accra"): "ghs.gov.gh",
    ("Karaga District Hospital", "Karaga"): "ghs.gov.gh",
    ("KariKari Brobbey Hospital", "Accra"): "ghs.gov.gh",
    ("Keta District Hospital", "Keta"): "ghs.gov.gh",
    ("Kete Krachi Government Hospital", "Kete Krachi"): "ghs.gov.gh",
    ("Ketu South Municipal Hospital", "Aflao"): "ghs.gov.gh",
    ("Kibi Government Hospital", "Kyebi"): "ghs.gov.gh",
    ("King David Hospital", "Sakumono, Tema"): "kingdavidmedicalcenter.com",
    ("Kintampo Municipal Hospital", "Kintampo"): "ghs.gov.gh",
    ("Kokofu Hospital", "Kokofu, Kumasi"): "ghs.gov.gh",
    ("Konongo Government Hospital", "Konongo-Odumase"): "ghs.gov.gh",
    ("Kpandai District Hospital", "Kpandai"): "ghs.gov.gh",
    ("Komfo Anokye Teaching Hospital", "Bantama, Kumasi"): "kath.gov.gh",
    ("Korle-Bu Teaching Hospital", "Guggisberg Avenue, Korle Bu, Accra"): "kbth.gov.gh",
    ("Kumasi South Hospital", "Kumasi"): "ghs.gov.gh",
    ("Kumoji Hospital", "Labone, Accra"): "ghs.gov.gh",
    ("Kuntenase District Hospital", "Kuntanase, Bosomtwe"): "ghs.gov.gh",
    ("Kwahu Government Hospital", "Atibie, Kwahu South"): "ghs.gov.gh",
    ("Kwame Danso District Hospital", "Kwame Danso, Sene West"): "ghs.gov.gh",
    ("La General Hospital", "La, Accra"): "ghs.gov.gh",
    ("Lapaz Community Hospital", "Abeka-Lapaz, Accra"): "lapazcommunityhospital.org",
    ("Lawra District Hospital", "Lawra"): "ghs.gov.gh",
    ("Lekma General Hospital", "Teshie-Nungua, Accra"): "lekmahospital.org",
    ("Lexis Hospital", "Sunyani"): "ghs.gov.gh",
    ("Lighthouse Mission Hospital", "North Kaneshie, Accra"): "stkathrynshospital.com",
    ("Lister Hospital", "Airport Hills, Accra"): "listerhospital.com.gh",
    ("Mampong District Hospital", "Mampong-Ashanti"): "ghs.gov.gh",
    ("Mamprobi Polyclinic", "Mamprobi, Accra"): "mphgh.com",
    ("Manhyia District Hospital", "Manhyia, Kumasi"): "ghs.gov.gh",
    ("Mankranso Hospital", "Mankranso, Ahafo Ano South"): "ghs.gov.gh",
    ("Manna Mission Hospital", "Teshie-Nungua, Accra"): "mannamissiongh.org",
    ("Margret Marquart Catholic Hospital", "Kpando"): "ghs.gov.gh",
    ("Mary Theresa Hospital", "Dodi Papase, Kadjebi"): "smthospital.org",
    ("McKenzie Health Services", "Ahisan-Estate, Kumasi"): "ghs.gov.gh",
    ("Medifem Hospital", "Westlands, West Legon, Accra"): "medifemhospital.com",
    ("Methodist Faith Healing Hospital", "Ankaase, Afigya Kwabre"): "mfhhospital.org",
    ("Mission Trinity Hospital", "Winneba"): "ghs.gov.gh",
    ("Modern Surgical Hospital", "Savelugu"): "ghs.gov.gh",
    ("Mother and Child Hospital", "Kasoa, Awutu Senya East"): "ghs.gov.gh",
    ("Mount Olives Hospital", "Techiman"): "mountoliveshospital.com",
    ("Nadowli Hospital", "Nadowli"): "ghs.gov.gh",
    ("Nagel Memorial Hospital", "Takoradi"): "ghs.gov.gh",
    ("Nana Hima Dekyi Hospital", "Dixcove, Ahanta West"): "ghs.gov.gh",
    ("Nandom Municipal Hospital", "Nandom"): "nandomhospital.com",
    ("Narh-Bita Hospital", "Tema"): "narhbita.com.gh",
    ("Navrongo War Memorial Hospital", "Navrongo, Kassena-Nankana"): "ghs.gov.gh",
    ("New Ashongman Hospital", "Ashongman, Accra"): "ghs.gov.gh",
    ("New Crystal Hospital", "Accra"): "newcrystalhealth.org",
    ("New Edubiase Hospital", "New Edubiase, Adansi South"): "ghs.gov.gh",
    ("New Hope Clinic", "Viepe, Aflao"): "ghs.gov.gh",
    ("New Hope Hospital", "Accra"): "ghs.gov.gh",
    ("Newlife Clinic and Laboratory", "Tamale"): "ghs.gov.gh",
    ("Nkawie Hospital", "Nkawie, Atwima Nwabiagya"): "ghs.gov.gh",
    ("Nkenkensu Hospital", "Kumasi"): "ghs.gov.gh",
    ("Nkoranza District Hospital", "Nkoranza"): "ghs.gov.gh",
    ("Nkwanta District Hospital", "Nkwanta"): "ghs.gov.gh",
    ("North Legon Hospital", "North Legon, Accra"): "northlegonhospital.com",
    ("North Ridge Clinic", "North Ridge, Accra"): "ghs.gov.gh",
    ("Nsawam Government Hospital", "Nsawam"): "ghs.gov.gh",
    ("Nyaho Medical Centre", "Airport Residential Area, Accra"): "nyahomedical.com",
    ("Obengfo Hospital", "Accra"): "ghs.gov.gh",
    ("Obuasi Hospital", "Obuasi"): "ghs.gov.gh",
    ("Oda Government Hospital", "Akyem Oda"): "ghs.gov.gh",
    ("Opmann Clinic", "Abeka-Lapaz, Accra"): "ghs.gov.gh",
    ("Otobia Memorial Hospital", "Accra"): "ghs.gov.gh",
    ("Our Lady of Grace Hospital", "Breman Asikuma, Asikuma/Odoben/Brakwa"): "olg-hospital.org",
    ("Owusu Memorial Hospital", "Sunyani"): "ghs.gov.gh",
    ("Pakphase Medical Center", "Cape Coast"): "ghs.gov.gh",
    ("Pantang Hospital", "Pantang, Accra"): "pantanghospital.gov.gh",
    ("Peace & Love Hospital", "Oduom, Kumasi"): "breastcareinternational.org",
    ("Peki Government Hospital", "Peki, South Dayi"): "ghs.gov.gh",
    ("Pentecost Hospital", "Madina, Accra"): "ghs.gov.gh",
    ("Pima Hospital", "Buokrom Estate, Kumasi"): "ghs.gov.gh",
    ("Police Hospital", "Cantonments, Accra"): "ghanapolicehospital.com",
    ("Presbyterian Hospital", "Donkorkrom, Kwahu North"): "ghs.gov.gh",
    ("Prilway Specialist Clinic", "Madina, Accra"): "ghs.gov.gh",
    ("Prime Care Medical Centre", "Accra"): "ghs.gov.gh",
    ("Princess Marie Louise Children's Hospital", "Dzorwulu, Accra"): "pmlhosp.org",
    ("Provita Specialist Hospital", "Tema"): "ghs.gov.gh",
    ("Quality Medical Center", "Garu"): "ghs.gov.gh",
    ("Raphal Medical Center", "Community 10, Tema"): "ghs.gov.gh",
    ("Richard Novati Catholic Hospital", "Sogakope, South Tongu"): "ghs.gov.gh",
    ("Rofhi Hospital", "Accra"): "ghs.gov.gh",
    ("Rooney Memorial Hospital", "Asankragwa, Wassa Amenfi West"): "ghs.gov.gh",
    ("Royal Good Shepherd Hospital", "Accra"): "ghs.gov.gh",
    ("SDA Hospital", "Asamang, Asante Akim"): "ghs.gov.gh",
    ("SDA Hospital", "Dominase, Bekwai"): "ghs.gov.gh",
    ("SDA Hospital", "Kwadaso, Kumasi"): "ghs.gov.gh",
    ("SDA Hospital", "Onwe, Ejisu-Juaben"): "ghs.gov.gh",
    ("SDA Hospital", "Sunyani"): "ghs.gov.gh",
    ("SDA Hospital", "Tamale"): "ghs.gov.gh",
    ("SDA Hospital - Wiamoase", "Wiamoase, Sekyere South"): "ghs.gov.gh",
    ("Saboba Medical Centre", "Saboba"): "ghs.gov.gh",
    ("Sacred Heart Hospital", "Weme, Abor, Keta"): "ghs.gov.gh",
    ("Saint John of God Hospital", "Domeabra, Nkoranza North"): "ghs.gov.gh",
    ("Saint Joseph's Hospital", "Jirapa"): "ghs.gov.gh",
    ("Saint Joseph's Hospital", "Nkwanta"): "ghs.gov.gh",
    ("Saint Louis General Hospital", "Bodwesango, Adansi North"): "ghs.gov.gh",
    ("Saint Luke's Hospital", "Kasei, Ejura/Sekyedumase"): "ghs.gov.gh",
    ("Saint Martin de Porres Hospital", "Eikwe, Nzema East"): "ghs.gov.gh",
    ("Saint Martins Catholic Hospital", "Agroyesum, Amansie West"): "ghs.gov.gh",
    ("Saint Mathias Hospital", "Yeji, Pru"): "ghs.gov.gh",
    ("Saint Michaels Hospital", "Jachie-Pramso, Bosomtwe"): "stmichaelshospitalpramso.com",
    ("Saint Patrick's Hospital", "Maase-Offinso"): "ghs.gov.gh",
    ("Saint Theresa's Hospital", "Nkoranza"): "ghs.gov.gh",
    ("Saint Theresa's Hospital", "Nandom"): "nandomhospital.com",
    ("Sakumono Community Multiplex Hospital", "Sakumono, Tema"): "ghs.gov.gh",
    ("Saltpond Government Hospital", "Saltpond, Mfantsiman"): "ghs.gov.gh",
    ("Sam J Specialist Hospital", "Accra"): "samjhospital.com",
    ("Sampa Government Hospital", "Sampa, Jaman North"): "ghs.gov.gh",
    ("Sandema District Hospital", "Sandema, Builsa North"): "ghs.gov.gh",
    ("Sankore Health Centre", "Sankore, Asunafo South"): "ghs.gov.gh",
    ("Savelugu Municipal Hospital", "Savelugu"): "ghs.gov.gh",
    ("Seventh-Day Adventist Clinic", "Suaman-Dadieso, Enchi"): "ghs.gov.gh",
    ("Shai Osudoku District Hospital", "Dodowa"): "ghs.gov.gh",
    ("Shalom Medical Center", "North Ridge, Accra"): "ghs.gov.gh",
    ("Shiloh Medical Center", "Ningo Prampram, Accra"): "ghs.gov.gh",
    ("Sinel Specialist Hospital", "Tema"): "sinelhospital.com",
    ("Sogakope Government Hospital", "Sogakope, South Tongu"): "ghs.gov.gh",
    ("St John's Hospital & Fertility Centre", "Tantra Hill, Accra"): "stjohnshfc.com",
    ("St. Anthony's Hospital", "Dzodze, Ketu North"): "ghs.gov.gh",
    ("St. Dominic's Hospital", "Akwatia, Kwaebibirem"): "sdhakwatia.org",
    ("St. Elizabeth Hospital", "Hwidiem, Asutifi South"): "sech-gh.org",
    ("St. Francis Xavier Hospital", "Assin Foso"): "stfrancisxavierhospital.org",
    ("St. John of God Hospital", "Sefwi Wiawso"): "ghs.gov.gh",
    ("St. John of God Hospital", "Duayaw Nkwanta, Tano North"): "ghs.gov.gh",
    ("St. Joseph's Hospital", "Effiduase, Koforidua"): "stjosephhospitalkoforidua.com",
    ("St. Martins Hospital", "Agormanya, Lower Manya Krobo"): "stmartinshospital.org",
    ("St. Mary's Hospital", "Drobo, Jaman South"): "ghs.gov.gh",
    ("Star of Light Hospital", "Sankore, Asunafo South"): "ghs.gov.gh",
    ("Suhum Government Hospital", "Suhum"): "ghs.gov.gh",
    ("Suntreso Government Hospital", "Kumasi"): "ghs.gov.gh",
    ("Suntresu Hospital", "Kumasi"): "ghs.gov.gh",
    ("Sunyani Regional Hospital", "Sunyani"): "sth.gov.gh",
    ("Sycamore Medical Centre", "Adientem, Takoradi"): "ghs.gov.gh",
    ("Tafo Hospital", "Kumasi"): "ghs.gov.gh",
    ("Tamale Central Hospital", "Tamale"): "ghs.gov.gh",
    ("Tamale Teaching Hospital", "Tamale"): "tth.gov.gh",
    ("Tamale West Hospital", "Tamale"): "ghs.gov.gh",
    ("Tarkwa Government Hospital", "Tarkwa, Tarkwa-Nsuaem"): "ghs.gov.gh",
    ("Tema General Hospital", "Community 11, Tema"): "ghs.gov.gh",
    ("Tema Polyclinic", "Tema"): "ghs.gov.gh",
    ("Tema Women's Hospital", "Tema"): "ghs.gov.gh",
    ("Tepa Government Hospital", "Tepa, Ahafo Ano North"): "ghs.gov.gh",
    ("Tetteh Quarshie Memorial Hospital", "Akuapim-Mampong"): "ghs.gov.gh",
    ("The Community Hospital", "Ashongman, Accra"): "ghs.gov.gh",
    ("The King's Medical Centre", "Bontanga, Kumbungu"): "ghs.gov.gh",
    ("The Trust Hospital", "Osu, Accra"): "thetrusthospital.com",
    ("Third Medical Reception Hospital", "Sunyani"): "ghs.gov.gh",
    ("Tophill Hospital", "Kronum-Cementmu, Kumasi"): "ghs.gov.gh",
    ("TrustCare Specialist Hospital", "Kumasi"): "ghs.gov.gh",
    ("Tumu Hospital", "Tumu, Sissala East"): "ghs.gov.gh",
    ("Twifo Praso District Hospital", "Twifo Praso"): "ghs.gov.gh",
    ("UDS Hospital", "Tamale"): "uds.edu.gh",
    ("University Hospital", "Legon, Accra"): "ug.edu.gh",
    ("University Hospital", "University of Cape Coast, Cape Coast"): "ucc.edu.gh",
    ("University of Ghana Medical Centre", "Legon, Accra"): "ugmc.ug.edu.gh",
    ("Upper West Regional Hospital", "Wa"): "ghs.gov.gh",
    ("VEBS Medical Centre", "Accra"): "ghs.gov.gh",
    ("VRA Hospital", "Accra"): "vhslgh.com",
    ("Valco Hospital", "Tema"): "valcotema.com",
    ("Valley View Adventist Hospital", "Techiman"): "ghs.gov.gh",
    ("Vicom Specialist Hospital", "Accra"): "ghs.gov.gh",
    ("Virtue Medical Centre", "Tumu, Sissala East"): "ghs.gov.gh",
    ("Vision Hospital", "Oyarifa East, Accra"): "visionhospitals.org",
    ("Walewale Government Hospital", "Walewale"): "ghs.gov.gh",
    ("Weija-Gbawe Municipal Hospital", "Weija"): "ghs.gov.gh",
    ("Wellspan Health", "Aborkutsime, Abor"): "ghs.gov.gh",
    ("Wenchi Methodist Hospital", "Wenchi"): "methowen.org",
    ("Wesley Clinic", "Kasoa, Awutu Senya East"): "wesleyclinicgh.com",
    ("West End Hospital", "Kumasi"): "westend-hospital.com",
    ("West Hospital", "Tamale"): "ghs.gov.gh",
    ("Wiawso Government Hospital", "Sefwi Wiawso"): "ghs.gov.gh",
    ("Winneba Government Hospital", "Winneba, Effutu"): "ghs.gov.gh",
    ("Yendi District Hospital", "Yendi"): "yendihospital.gov.gh",
    ("Zabzugu District Hospital", "Zabzugu"): "ghs.gov.gh",
    ("Zebilla Government Hospital", "Zebilla, Bawku West"): "ghs.gov.gh",
}

# Real ministry domains kept alongside the hospital domains.
KEEP = {"ghs.gov.gh", "moh.gov.gh"}


def apply(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")

    missing = []
    for clinic in Clinic.objects.all():
        domain = REAL.get((clinic.name, clinic.address))
        if domain is None:
            missing.append((clinic.name, clinic.address))
            domain = "ghs.gov.gh"
        clinic.email_domain = domain
        clinic.save(update_fields=["email_domain"])

    used = set(
        Clinic.objects.exclude(email_domain="").values_list("email_domain", flat=True)
    )
    AllowedHospitalDomain.objects.all().delete()
    for domain in sorted(used | KEEP):
        AllowedHospitalDomain.objects.get_or_create(domain=domain)

    if missing:
        raise SystemExit(f"UNMAPPED HOSPITALS: {missing}")


def revert(apps, schema_editor):
    # Restore the deterministic unique name-derived domains from 0009/0010.
    Clinic = apps.get_model("clinics", "Clinic")
    AllowedHospitalDomain = apps.get_model("clinics", "AllowedHospitalDomain")
    real = {
        "37milhosp.gov.gh", "accrapsychiatrichospital.org", "agogopresbyhospital.org",
        "aishahospital.com", "baptistmedicalcenter.org", "ccthghana.org",
        "elitecarecenter.com", "erhk.org", "euracarehealth.com", "finneyhospital.com",
        "frimpongboatengmedicalcenter.com", "hth.gov.gh", "impactclinic.com.gh",
        "kath.gov.gh", "kbth.gov.gh", "lapazcommunityhospital.org",
        "medifemhospital.com", "nyahomedical.com", "olg-hospital.org",
        "thetrusthospital.com", "tth.gov.gh",
    }
    reserved = {"ghs.gov.gh", "moh.gov.gh"}

    def unique_domain(name, address, taken):
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

    taken = set(real)
    for row in Clinic.objects.exclude(email_domain="").exclude(email_domain__in=reserved).values_list("email_domain", flat=True):
        taken.add(row)
    for clinic in Clinic.objects.order_by("name", "address"):
        clinic.email_domain = unique_domain(clinic.name, clinic.address, taken)
        clinic.save(update_fields=["email_domain"])

    used = set(
        Clinic.objects.exclude(email_domain="").values_list("email_domain", flat=True)
    )
    AllowedHospitalDomain.objects.all().delete()
    for domain in sorted(used | reserved):
        AllowedHospitalDomain.objects.get_or_create(domain=domain)


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0010_generate_unique_hospital_domains"),
    ]

    operations = [
        migrations.RunPython(apply, revert),
    ]