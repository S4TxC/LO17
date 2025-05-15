import re
import json
import xml.etree.ElementTree as ET
import unicodedata
import os
import difflib

def charger_lexique(fichier):
    lexique = {}
    with open(fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            mot, lemme = ligne.strip().split('\t')
            lexique[mot.lower()] = lemme.lower()
    return lexique

def distance_levenshtein(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def chercher_candidats_par_prefixe(mot, lexique):
    candidats = []
    for lex_mot in lexique:
        prefixe = len(os.path.commonprefix([mot, lex_mot]))
        if prefixe >= 2:
            candidats.append(lex_mot)
    return candidats

def lemmatiser_phrase(phrase, lexique):
    mots = phrase.strip().split()
    resultats = {}
    for mot in mots:
        mot_clean = ''.join(c for c in mot.lower() if c.isalpha())
        if not mot_clean:
            continue
        if mot_clean in lexique:
            resultats[mot] = lexique[mot_clean]
        else:
            candidats = chercher_candidats_par_prefixe(mot_clean, lexique)
            if not candidats:
                resultats[mot] = "Aucun lemme trouvé"
            elif len(candidats) == 1:
                resultats[mot] = lexique[candidats[0]]
            else:
                meilleur = max(candidats, key=lambda w: distance_levenshtein(mot_clean, w))
                resultats[mot] = lexique[meilleur]
    return resultats

# === Chargement du lexique ===
LEXIQUE = charger_lexique("TxtFiles/LemmatisationSpaCy.txt")

# === Extraction des rubriques depuis XML ===
def extraire_rubriques_depuis_xml(fichier_xml="corpus2.xml"):
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    rubriques = set()
    for bulletin in root.findall('bulletin'):
        rubrique = bulletin.find('rubrique')
        if rubrique is not None:
            rubriques.add(rubrique.text.strip())
    return list(rubriques)

RUBRIQUES = extraire_rubriques_depuis_xml()

MOTS_VIDES = {
    "je", "nous", "vous", "tu", "ils", "elles", "on",
    "veux", "voudrais", "souhaite", "souhaiterais", "souhaites", "souhaitons",
    "cherche", "cherchons", "chercher", "trouver", "trouvez", "trouvons",
    "donner", "donne", "donnez", "afficher", "affiche", "voir", "liste", "lister",
    "articles", "article", "bulletins", "bulletin",
    "les", "des", "le", "la", "un", "une", "du", "de", "d'", "l'", "aux", "au", "à", "en", "dans",
    "par", "sur", "concernant", "portant", "traitant", "parlant", "mentionnant", "évoquant", "impliquant",
    "qui", "que", "dont", "quoi", "où", "avec",
    "sont", "est", "été", "être", "sera", "seront", "ont", "a", "ont été",
    "et", "ou", "mais", "pas", "soit", "non", "ne",
    "ce", "cet", "cette", "ces", "quel", "quelle", "quels", "quelles", "tout", "tous", "toutes",
    "contenu", "contenant", "possédant", "provenant", "écrits", "publiés", "publié", "publiée",
    "mois", "année", "titre", "rubrique", "rubriques", "l", "pour", "sous", "vers", "parler", "parlent"
}

def normaliser_texte(texte):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texte.lower())
        if unicodedata.category(c) != 'Mn'
    )

def extraire_dates(requete):
    requete = requete.lower()
    patterns = {
        "jj_mm_aaaa": r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        "jour_mois_annee": r'\b\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b',
        "mois_annee": r'\b(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b',
        "annee": r'\b\d{4}\b'
    }
    dates_detectees = set()
    for pattern in patterns.values():
        matches = re.findall(pattern, requete)
        for match in matches:
            if not any(match in d and match != d for d in dates_detectees):
                dates_detectees.add(match)
    return list(dates_detectees)

def extraire_periode(requete, dates):
    requete = requete.lower()
    mois_regex = r"(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)"
    exclusion = None
    exclu = re.search(r"(?:mais pas|sauf)\s+(?:au|en)?\s*(?:mois de\s+)?" + mois_regex, requete)
    if exclu:
        exclusion = exclu.group(1)
    if len(dates) >= 2 and "entre" in requete:
        debut, fin = sorted(dates)[:2]
        return {"type": "intervalle", "debut": debut, "fin": fin, "exclusion": exclusion}
    elif "après" in requete and dates:
        return {"type": "après", "valeur": dates[0]}
    elif "avant" in requete and dates:
        return {"type": "avant", "valeur": dates[0]}
    elif len(dates) == 1:
        return {"type": "exacte", "valeur": dates[0]}
    return None

def extraire_rubrique(requete):
    requete_norm = normaliser_texte(requete)
    for rubrique in RUBRIQUES:
        rubrique_norm = normaliser_texte(rubrique)
        mots_rubrique = rubrique_norm.split()
        if all(mot in requete_norm for mot in mots_rubrique):
            return rubrique
    return None

def extraire_mots_cles(requete):
    mots = re.findall(r'\b\w+\b', requete.lower())
    mots_utiles = [
        mot for mot in mots
        if mot not in MOTS_VIDES and mot not in [r.lower() for r in RUBRIQUES]
    ]
    texte_a_corriger = ' '.join(mots_utiles)
    corrections = lemmatiser_phrase(texte_a_corriger, LEXIQUE)
    return list(set(corrections.values()) - {"Aucun lemme trouvé"})

def detecter_operateur(requete):
    requete = requete.lower()
    if " ou " in requete:
        return "OU"
    elif " mais pas " in requete or " pas " in requete:
        return "ET -"
    elif " et " in requete:
        return "ET"
    return "ET"

def rechercher_documents(structure_requete, fichier_xml="corpus2.xml"):
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    resultats = []

    for bulletin in root.findall('bulletin'):
        contenu = bulletin.find('tokenisation').text.lower() if bulletin.find('tokenisation') is not None else ""
        rubrique = bulletin.find('rubrique').text.strip() if bulletin.find('rubrique') is not None else ""
        date = bulletin.find('date').text.strip() if bulletin.find('date') is not None else ""

        correspond = True

        # Filtrage par mots-clés selon l'opérateur logique
        mots_cles = structure_requete["mots_cles"]
        if mots_cles:
            if structure_requete["operateur_logique"] == "ET":
                correspond &= all(mot in contenu for mot in mots_cles)
            elif structure_requete["operateur_logique"] == "OU":
                correspond &= any(mot in contenu for mot in mots_cles)
            elif structure_requete["operateur_logique"] == "ET -":
                positif = [mot for mot in mots_cles if "-" not in mot]
                negatif = [mot[1:] for mot in mots_cles if mot.startswith("-")]
                correspond &= all(m in contenu for m in positif) and all(m not in contenu for m in negatif)

        # Filtrage par rubrique
        if structure_requete["rubrique"]:
            correspond &= structure_requete["rubrique"].lower() in rubrique.lower()

        # (Simplifié) Filtrage par date (présence de la chaîne dans la date du bulletin)
        if structure_requete["dates"]:
            if not any(d in date for d in structure_requete["dates"]):
                correspond = False

        if correspond:
            titre = bulletin.find('titre').text.strip() if bulletin.find('titre') is not None else "(Sans titre)"
            resultats.append({"titre": titre, "date": date, "rubrique": rubrique})

    return resultats

def traiter_requete(requete):
    dates = extraire_dates(requete)
    return {
        "dates": dates,
        "rubrique": extraire_rubrique(requete),
        "mots_cles": extraire_mots_cles(requete),
        "operateur_logique": detecter_operateur(requete),
        "periode": extraire_periode(requete, dates)
    }

if __name__ == "__main__":
    requete = input("Entrez votre requête en langage naturel :\n")
    structure = traiter_requete(requete)
    print("\nStructure extraite :")
    print(json.dumps(structure, indent=4, ensure_ascii=False))

    resultats = rechercher_documents(structure)
    print("\nDocuments trouvés :")
    for doc in resultats:
        print(f"- {doc['titre']} ({doc['date']} / {doc['rubrique']})")