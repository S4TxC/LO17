#####################################################################################################

############################### Fichier pour créer l'antidictionnaire ###############################

#####################################################################################################

# seuil = 0.00109                                       # Valeur Q1 ==> Trop de stopwords

# seuil = 0.00109/2.25                                  # 2.5 ==> 144 SW | 2.3 ==> 164 SW | 2.1 ==> 201 SW | 2.2 ==> 179 SW | 2.25 ==> 168 SW

seuil = 0.0127/23

fichier_tf_idf = "TxtFiles/tf_idf2.txt"                          #"TxtFiles/X3 - tf_idf.txt"
fichier_stopwords = "TxtFiles/stopwords2.txt"                    #"TxtFiles/X4 - stopwords.txt"

stopwords = set()

# Lecture du fichier TF-IDF
with open(fichier_tf_idf, "r", encoding="utf-8") as f:
    for ligne in f:
        _, mot, tfidf = ligne.strip().split("\t")
        if float(tfidf) <= seuil:
            stopwords.add(mot)

# Sauvegarde des stopwords
with open(fichier_stopwords, "w", encoding="utf-8") as f:
    for mot in sorted(stopwords):
        f.write(mot + "\n")

print(f"{len(stopwords)} stopwords identifiés et enregistrés dans le fichier : {fichier_stopwords}")
