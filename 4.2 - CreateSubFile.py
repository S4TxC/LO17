def generate_substitution_file(fichier_stopwords, fichier_substitution):
    stopwords = set()
    with open(fichier_stopwords, 'r', encoding='utf-8') as f:
        for line in f:
            stopwords.add(line.strip())                                         # Ajouter chaque mot à la liste des stopwords

    # Créer le fichier de substitution
    with open(fichier_substitution, 'w', encoding='utf-8') as f:
        for stopword in stopwords:
            f.write(f"{stopword}\t''\n")                                        # Remplacer les stopwords par une chaîne vide ("")

fichier_stopwords = "X4 - stopwords.txt"
fichier_substitution = "X5 - substitution.txt"

generate_substitution_file(fichier_stopwords, fichier_substitution)