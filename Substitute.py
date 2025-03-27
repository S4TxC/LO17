""" 
import sys

def charger_substitution(fichier_substitution):
    substitutions = {}
    with open(fichier_substitution, 'r', encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().split('\t')
            if len(parts) == 2:  # Vérification du format
                mot, remplacement = parts
                substitutions[mot] = remplacement
    return substitutions

def substituer_tokens(fichier_tokens, fichier_substitution, fichier_sortie):
    #Remplace ou supprime les mots selon le dictionnaire de substitution.
    substitutions = charger_substitution(fichier_substitution)

    with open(fichier_tokens, 'r', encoding="utf-8") as f_in, open(fichier_sortie, 'w', encoding="utf-8") as f_out:
        for ligne in f_in:
            try:
                token, bulletin_num = ligne.strip().split('\t')
                remplacement = substitutions.get(token, token)  # Remplacement si trouvé
                if remplacement:  # Si le mot n'est pas supprimé
                    f_out.write(f"{remplacement}\t{bulletin_num}\n")
            except ValueError:
                continue  # Ignore les lignes mal formatées

if len(sys.argv) != 4:
    print("Erreur, manque arguments suivre syntaxe : python .\Substitue.py <fichier_tokens> <fichier_substitution> <fichier_sortie>")
    sys.exit(1)

substituer_tokens(sys.argv[1], sys.argv[2], sys.argv[3])
 """

def charger_substitution(fichier_substitution):
    # Charger les mots à remplacer (ou supprimer) depuis le fichier de substitution
    substitutions = {}
    with open(fichier_substitution, 'r', encoding='utf-8') as f:
        for ligne in f:
            mot, remplacement = ligne.strip().split('\t')
            substitutions[mot] = remplacement
    return substitutions

def substituer_tokens(fichier_tokens, fichier_substitution, fichier_sortie):
    # Charger les substitutions
    substitutions = charger_substitution(fichier_substitution)
    
    with open(fichier_tokens, 'r', encoding='utf-8') as f, open(fichier_sortie, 'w', encoding='utf-8') as sortie:
        for ligne in f:
            token, bulletin_num = ligne.strip().split('\t')
            if token in substitutions:
                replacement = substitutions[token]  # Récupérer la substitution
                if replacement:  # Si remplacement n'est pas une chaîne vide
                    sortie.write(f"{replacement}\t{bulletin_num}\n")
            else:
                sortie.write(f"{token}\t{bulletin_num}\n")  # Si le mot n'est pas un stopword, on garde le token

# Exemple d'utilisation
fichier_tokens = "test.txt"  # Fichier contenant les tokens générés par segmente.py
fichier_substitution = "X5 - substitution.txt"  # Le fichier de substitution généré par generate_substitution.py
fichier_sortie = "X6 - TokensFiltres.txt"  # Le fichier de sortie contenant les tokens filtrés

substituer_tokens(fichier_tokens, fichier_substitution, fichier_sortie)