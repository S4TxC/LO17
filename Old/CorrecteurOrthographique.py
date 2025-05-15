import difflib
import os

def charger_lexique(fichier):
    lexique = {}
    with open(fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            mot, lemme = ligne.strip().split('\t')
            lexique[mot.lower()] = lemme.lower()
    return lexique

# Distance de Levenshtein
def distance_levenshtein(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

# Recherche par préfixe
def chercher_candidats_par_prefixe(mot, lexique):
    candidats = []
    for lex_mot in lexique:
        prefixe = len(os.path.commonprefix([mot, lex_mot]))
        if prefixe >= 2:                                                                                           # Ajuster ce seuil pour un meilleur affinage
            candidats.append(lex_mot)
    return candidats

def lemmatiser_phrase(phrase, lexique):
    mots = phrase.strip().split()
    resultats = {}

    for mot in mots:
        mot_clean = ''.join(c for c in mot.lower() if c.isalpha())                                                 # Nettoyer ponctuation
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
                meilleur = max(candidats, key=lambda w: distance_levenshtein(mot_clean, w))                         # Comparaison par Levenshtein
                resultats[mot] = lexique[meilleur]

    return resultats


lexique = charger_lexique("TxtFiles/LemmatisationSpaCy.txt")
phrase = input("Entrez une phrase : ")
lemmes = lemmatiser_phrase(phrase, lexique)

print("\nRésultat :")
for mot, lemme in lemmes.items():
    print(f"{mot} -> {lemme}")