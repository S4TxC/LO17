                ####### Fichier du moteur de recherche #######

import re
import json
from collections import defaultdict
import unicodedata
import xml.etree.ElementTree as ET

def extraire_rubriques(fichier_xml="Corpus/corpusV3.xml"):
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
    "je", "nous", "vous", "tu", "ils", "elles", "on", "partir",
    "veux", "voudrais", "souhaite", "souhaiterais", "souhaites", "souhaitons",
    "cherche", "cherchons", "chercher", "rechercher", "trouver", "trouvez", "trouvons",
    "donner", "donne", "donnez", "afficher", "affiche", "voir", "liste", "lister",
    "articles", "article", "bulletins", "bulletin", "parus", "propos",
    "les", "des", "le", "la", "un", "une", "du", "de", "d'", "l'", "aux", "au", "à", "en", "dans", "d",
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
    mots_filtres = [mot for mot in mots if mot not in Stopwords]
    
    rubrique = extraire_rubrique(requete)
    if rubrique:
        mots_rubrique = re.findall(r'\b\w+\b', rubrique.lower())
        mots_filtres = [mot for mot in mots_filtres if mot not in mots_rubrique]

    dates = extraire_dates(requete)
    dates_mots = set()
    for d in dates:
        dates_mots.update(re.findall(r'\b\w+\b', d.lower()))
    mots_filtres = [mot for mot in mots_filtres if mot not in dates_mots]

    return mots_filtres

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

def charger_index(fichier):
    index = defaultdict(dict)
    with open(fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            term, doc_list, total = ligne.strip().split("\t")
            term = term.strip()
            docs = doc_list.split(", ")
            for doc in docs:
                doc_id, freq = doc.split(":")
                index[term][doc_id] = int(freq)
    return index

def interroger_index(index, termes):
    resultats = set()
    for terme in termes:
        normalisation = normaliser_texte(terme)
        for key in index.keys():
            if normaliser_texte(key) == normalisation:
                resultats.update(index[key].keys())
    return resultats

def requete_cible_titre(requete):
    requete = requete.lower()
    return any(kw in requete for kw in ["dans le titre", "titre contient", "titre", "au titre"])

def variantes_terme(mot):
    var = set()
    var.add(mot)
    if mot.endswith('s'):
        var.add(mot[:-1])
    else:
        var.add(mot + 's')
    return var


def rechercher_documents(requete):
    index_titre = charger_index('index_inverses/index_titre.txt')
    index_rubrique = charger_index('index_inverses/index_rubrique.txt')
    index_date = charger_index('index_inverses/index_date.txt')
    index_lemmes = charger_index('index_inverses/index_lemmes.txt')

    resultat_requete = traiter_requete(requete)
    cible_titre = requete_cible_titre(requete)
    mots_cles = resultat_requete['mots_cles']
    periode = resultat_requete['periode']
    rubrique = resultat_requete['rubrique']
    operateur_logique = resultat_requete['operateur_logique']

    print(f"Mots-clés extraits : {mots_cles}")
    print(f"Période extraite : {periode}")
    print(f"Rubrique extraite : {rubrique}")
    print(f"Opérateur logique : {operateur_logique}")
    print(f"Recherche ciblée sur le titre : {cible_titre}")

    documents_mots_cles = set()
    documents_rubrique = set()
    documents_date = set()

    tous_docs = set()
    for index in [index_lemmes, index_rubrique, index_date]:
        for docs in index.values():
            tous_docs.update(docs.keys())

    index_actif = index_titre if cible_titre else index_lemmes

    mots_cles = [
        mot for mot in mots_cles
        if any(
            variante in index_actif
            for variante in variantes_terme(mot)
        )
    ]

    if mots_cles:
        for mot in mots_cles:
            termes_recherche = variantes_terme(mot)
            docs_mot = set()
            for terme in termes_recherche:
                if terme in index_actif:
                    docs_mot.update(index_actif[terme].keys())           
            if not documents_mots_cles:
                documents_mots_cles = docs_mot
            else:
                if operateur_logique == "ET":
                    documents_mots_cles &= docs_mot
                elif operateur_logique == "OU":
                    documents_mots_cles |= docs_mot
                elif operateur_logique == "NON":
                    documents_mots_cles -= docs_mot

    if rubrique:
        documents_rubrique = interroger_index(index_rubrique, [rubrique])

    if periode:
        for date_val in index_date:
            if periode['type'] == 'exacte' and date_val == periode['valeur']:
                documents_date.update(index_date[date_val].keys())
            elif periode['type'] == 'intervalle' and periode['debut'] <= date_val <= periode['fin']:
                documents_date.update(index_date[date_val].keys())
            elif periode['type'] == 'avant' and date_val <= periode['valeur']:
                documents_date.update(index_date[date_val].keys())
            elif periode['type'] == 'après' and date_val >= periode['valeur']:
                documents_date.update(index_date[date_val].keys())

    # Fusion finale selon logique booléenne
    ensembles = [documents_mots_cles, documents_rubrique, documents_date]
    ensembles = [s for s in ensembles if s]  # Ne garder que les non vides

    if not ensembles:
        return []

    resultat_final = ensembles[0]
    for s in ensembles[1:]:
        if operateur_logique == "ET":
            resultat_final &= s
        elif operateur_logique == "OU":
            resultat_final |= s
        elif operateur_logique == "NON":
            resultat_final -= s

    return list(resultat_final)


if __name__ == "__main__":
    requete = input("Entrez votre requête :\n")
    resultat = rechercher_documents(requete)
    print("\nDocuments correspondants :")
    print(json.dumps(resultat, indent=4, ensure_ascii=False))