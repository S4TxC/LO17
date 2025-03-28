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