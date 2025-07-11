                ####### Fichier pour substituer les stopwords après segmentation #######

def charger_substitution(fichier_substitution):
    substitutions = {}
    with open(fichier_substitution, 'r', encoding='utf-8') as f:
        for ligne in f:
            mot, remplacement = ligne.strip().split('\t')
            substitutions[mot] = remplacement
    return substitutions

def substituer_tokens(fichier_tokens, fichier_substitution, fichier_sortie):
    substitutions = charger_substitution(fichier_substitution)
    
    with open(fichier_tokens, 'r', encoding='utf-8') as f, open(fichier_sortie, 'w', encoding='utf-8') as sortie:
        for ligne in f:
            token, bulletin_num = ligne.strip().split('\t')
            if token in substitutions:
                replacement = substitutions[token]                              # Récupérer la substitution
                if replacement:
                    sortie.write(f"{replacement}\t{bulletin_num}\n")
            else:
                sortie.write(f"{token}\t{bulletin_num}\n")                      # Si le mot n'est pas un stopword, on garde le token


fichier_tokens = "TxtFiles/segmente.txt"                                        # Fichier contenant les tokens générés par segmente.py
fichier_substitution = "TxtFiles/substitution.txt"                              # Fichier de substitution
fichier_sortie = "TxtFiles/tokenV1.txt"                                         # Fichier de sortie avec tokens filtrés
substituer_tokens(fichier_tokens, fichier_substitution, fichier_sortie)