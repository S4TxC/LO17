######################################################################################################################################################

############################### Fichier intermédiaire pour faire les substitutions dans la tokenisation déjà effectuée ###############################

######################################################################################################################################################

def generer_fichier_substitution(fichier_stopwords, fichier_substitution):
    stopwords = set()
    with open(fichier_stopwords, 'r', encoding='utf-8') as f:
        for line in f:
            stopwords.add(line.strip())                                         # Ajouter chaque mot à la liste des stopwords

    # Créer le fichier de substitution
    with open(fichier_substitution, 'w', encoding='utf-8') as f:
        for stopword in stopwords:
            f.write(f"{stopword}\t''\n")                                        # Remplacer les stopwords par une chaîne vide ("")

fichier_stopwords = "TxtFiles/stopwords2.txt"                                            #"TxtFiles/X4 - stopwords.txt"
fichier_substitution = "TxtFiles/sub2.txt"                                               #"TxtFiles/X5 - substitution.txt"
generer_fichier_substitution(fichier_stopwords, fichier_substitution)