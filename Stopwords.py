                ####### Fichier pour créer l'antidictionnaire #######

seuil = 0.00111/2.22                                               # Seuil obtenu en tatônnant

fichier_tf_idf = "TxtFiles/tf_idf.txt"
fichier_stopwords = "TxtFiles/stopwords.txt"

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