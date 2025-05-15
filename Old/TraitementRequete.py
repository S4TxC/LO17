import re
import json
import xml.etree.ElementTree as ET
import unicodedata

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
    "sont", "est", "été", "être", "sera", "seront", "ont", "a", "ont été", "ont été publiés",
    "et", "ou", "mais", "pas", "soit", "non", "ne", "pas",
    "de", "ce", "cet", "cette", "ces", "quel", "quelle", "quels", "quelles", "tout", "tous", "toutes",
    "dont", "contenu", "contenant", "possédant", "provenant", "écrits", "publiés", "publié", "publiée",
    "mois", "année", "titre", "rubrique", "rubriques", "l", "la", "le", "les",
    "a", "au", "aux", "en", "dans", "par", "pour", "avec", "sur", "sous", "vers", "parler", "parlant",
    "parle", "parlent"
}


def extraire_dates(requete):
    requete = requete.lower()
    patterns = {
        "jj_mm_aaaa": r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        "jour_mois_annee": r'\b\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b',
        "mois_annee": r'\b(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b',
        "annee": r'\b\d{4}\b'
    }

    dates_detectees = set()

    matches_jma = re.findall(patterns["jour_mois_annee"], requete)
    dates_detectees.update(matches_jma)

    matches_slash = re.findall(patterns["jj_mm_aaaa"], requete)
    dates_detectees.update(matches_slash)

    matches_ma = re.findall(patterns["mois_annee"], requete)
    for ma in matches_ma:
        if not any(ma in jma for jma in dates_detectees):
            dates_detectees.add(ma)

    matches_a = re.findall(patterns["annee"], requete)
    for a in matches_a:
        if not any(a in d for d in dates_detectees):
            dates_detectees.add(a)

    return list(dates_detectees)

def extraire_periode(requete, dates):
    requete_norm = requete.lower()
    if len(dates) >= 2 and ("entre" in requete_norm or "de" in requete_norm and "à" in requete_norm):           # Cas : entre X et Y ou de X à Y
        dates_triees = sorted(dates)
        return {"type": "intervalle", "debut": dates_triees[0], "fin": dates_triees[1]}
    
    elif any(mot in requete_norm for mot in ["après", "à partir de", "postérieur à"]):
        for date in dates:
            if f"après {date}" in requete_norm or f"à partir de {date}" in requete_norm or f"postérieur à {date}" in requete_norm:
                return {"type": "après", "valeur": date}
        if dates:
            return {"type": "après", "valeur": dates[0]}
    
    elif any(mot in requete_norm for mot in ["avant", "jusqu’à", "antérieur à"]):
        for date in dates:
            if f"avant {date}" in requete_norm or f"jusqu’à {date}" in requete_norm or f"antérieur à {date}" in requete_norm:
                return {"type": "avant", "valeur": date}
        if dates:
            return {"type": "avant", "valeur": dates[0]}
    
    elif len(dates) == 1:
        return {"type": "exacte", "valeur": dates[0]}                                                           # Une seule date : on déduit une période simple
    
    return None


def normaliser_texte(texte):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texte.lower())
        if unicodedata.category(c) != 'Mn'
    )

def extraire_rubrique(requete):
    requete_norm = normaliser_texte(requete)
    
    for rubrique in RUBRIQUES:
        rubrique_norm = normaliser_texte(rubrique)
        mots_rubrique = rubrique_norm.split()
        
        if all(mot in requete_norm for mot in mots_rubrique):
            return rubrique                                                                                     # Renvoyer la rubrique avec sa casse et accentuation d'origine
    
    return None

def extraire_mots_cles(requete):
    mots = re.findall(r'\b\w+\b', requete.lower())
    return [
        mot for mot in mots
        if mot not in MOTS_VIDES and mot not in [r.lower() for r in RUBRIQUES]
    ]

def detecter_operateur(requete):
    requete = requete.lower()
    if " ou " in requete:
        return "OU"
    elif " mais pas " in requete or " pas " in requete:
        return "ET -"
    elif " et " in requete:
        return "ET"
    return "ET"

def traiter_requete(requete):
    dates = extraire_dates(requete)
    structure = {
        "dates": dates,
        "periode": extraire_periode(requete, dates),
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