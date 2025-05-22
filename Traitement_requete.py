import re
import unicodedata
import json
import xml.etree.ElementTree as ET

def extraire_rubriques(fichier_xml="corpus2.xml"):
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    rubriques = set()
    
    for bulletin in root.findall('bulletin'):
        rubrique = bulletin.find('rubrique')
        if rubrique is not None:
            rubriques.add(rubrique.text.strip())
    
    return list(rubriques)

Rubriques = extraire_rubriques()

Stopwords = {
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

def extraire_dates(requete):
    requete = requete.lower()
    patterns = {
        "jj_mm_aaaa": r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        "jour_mois_annee": r'\b\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b',
        "mois_annee": r'\b(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b',
        "annee": r'\b\d{4}\b'
    }
    
    dates = set()
    for key, pattern in patterns.items():
        dates.update(re.findall(pattern, requete))
    
    return list(dates)

def extraire_periode(requete, dates):
    requete = requete.lower()
    if len(dates) >= 2 and ("entre" in requete or "de" in requete and "à" in requete):
        dates.sort()
        return {"type": "intervalle", "debut": dates[0], "fin": dates[1]}
    
    if "après" in requete or "avant" in requete:
        for date in dates:
            if f"après {date}" in requete:
                return {"type": "après", "valeur": date}
            if f"avant {date}" in requete:
                return {"type": "avant", "valeur": date}
    
    if len(dates) == 1:
        return {"type": "exacte", "valeur": dates[0]}
    
    return None

def normaliser_texte(texte):
    return ''.join(c for c in unicodedata.normalize('NFD', texte.lower()) if unicodedata.category(c) != 'Mn')

def extraire_rubrique(requete):
    requete = normaliser_texte(requete)
    for rubrique in Rubriques:
        if normaliser_texte(rubrique) in requete:
            return rubrique
    return None

def extraire_mots_cles(requete):
    mots = re.findall(r'\b\w+\b', requete.lower())
    return [mot for mot in mots if mot not in Stopwords and mot not in [r.lower() for r in Rubriques]]

def detecter_operateur(requete):
    requete = requete.lower()
    if " ou " in requete:
        return "OU"
    if "mais pas" in requete or "pas" in requete:
        return "NON"
    if " et " in requete:
        return "ET"
    return "ET"

def traiter_requete(requete):
    dates = extraire_dates(requete)
    return {
        "dates": dates,
        "periode": extraire_periode(requete, dates),
        "rubrique": extraire_rubrique(requete),
        "mots_cles": extraire_mots_cles(requete),
        "operateur_logique": detecter_operateur(requete)
    }


if __name__ == "__main__":
    requete = input("Entrez votre requête :\n")
    resultat = traiter_requete(requete)
    print("\nStructure extraite :")
    print(json.dumps(resultat, indent=4, ensure_ascii=False))
