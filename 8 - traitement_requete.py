import re
import json
import xml.etree.ElementTree as ET

# Fonction pour extraire dynamiquement toutes les rubriques du corpus XML
def extraire_rubriques_depuis_xml(fichier_xml="corpus2.xml"):
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    rubriques = set()
    for bulletin in root.findall('bulletin'):
        rubrique = bulletin.find('rubrique')
        if rubrique is not None:
            rubriques.add(rubrique.text.strip())
    return list(rubriques)

# Chargement dynamique des rubriques
RUBRIQUES = extraire_rubriques_depuis_xml()

def extraire_dates(requete):
    dates = []
    regex_dates = [
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        r'\b\d{4}\b',
        r'\b(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b'
    ]
    for pattern in regex_dates:
        matches = re.findall(pattern, requete, re.IGNORECASE)
        dates.extend(matches)
    return list(set(dates))

def extraire_rubrique(requete):
    for rubrique in RUBRIQUES:
        if rubrique.lower() in requete.lower():
            return rubrique
    return None

def extraire_mots_cles(requete):
    mots_vides = {
        "je", "veux", "voudrais", "souhaite", "articles", "parlant", "parle",
        "sur", "de", "qui", "les", "la", "le", "des", "du", "dont", "avec",
        "à", "au", "en", "et", "ou", "mais", "pas", "soit", "dans", "un", "une"
    }
    mots = re.findall(r'\b\w+\b', requete.lower())
    return [mot for mot in mots if mot not in mots_vides and mot not in [r.lower() for r in RUBRIQUES]]

def detecter_operateur(requete):
    if " ou " in requete.lower():
        return "OU"
    elif " et " in requete.lower():
        return "ET"
    elif " mais pas " in requete.lower() or " pas " in requete.lower():
        return "ET -"
    return "ET"

def traiter_requete(requete):
    structure = {
        "dates": extraire_dates(requete),
        "rubrique": extraire_rubrique(requete),
        "mots_cles": extraire_mots_cles(requete),
        "operateur_logique": detecter_operateur(requete)
    }
    return structure

if __name__ == "__main__":
    requete = input("Entrez votre requête en langage naturel :\n")
    resultat = traiter_requete(requete)
    print("\nStructure extraite :")
    print(json.dumps(resultat, indent=4, ensure_ascii=False))
