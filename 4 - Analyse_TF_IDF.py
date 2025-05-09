##################################################################################################################################################

############################### Fichier pour faire des statistiques et déterminer un seuil pour l'antidictionnaire ###############################

##################################################################################################################################################


import numpy as np
import matplotlib.pyplot as plt


fichier_tf_idf = "tf_idf2.txt"                                  #"X3 - tf_idf.txt"
tfidf_values = []

with open(fichier_tf_idf, "r", encoding="utf-8") as f:
    for ligne in f:
        _, _, tfidf = ligne.strip().split("\t")
        tfidf_values.append(float(tfidf))

tfidf_values = np.array(tfidf_values)


# Quelques statistiques                                         # Penser à ajouter d'autres statistiques
moyenne = np.mean(tfidf_values)
mediane = np.median(tfidf_values)
q1 = np.percentile(tfidf_values, 25)                            # Premier quartile (Q1)
q3 = np.percentile(tfidf_values, 75)                            # Troisième quartile (Q3)
ecart_type = np.std(tfidf_values)


print(f"Moyenne TF-IDF: {moyenne:.5f}")
print(f"Médiane TF-IDF: {mediane:.5f}")
print(f"1er quartile (Q1): {q1:.5f}")
print(f"3ème quartile (Q3): {q3:.5f}")
print(f"Écart-type: {ecart_type:.5f}")


# Histogramme
plt.figure(figsize=(10, 6))
plt.hist(tfidf_values, bins=50, color='skyblue', edgecolor='red', alpha=0.7)
plt.axvline(q1, color='yellow', linestyle='dashed', linewidth=1, label="Q1 (25%)")
plt.axvline(mediane, color='green', linestyle='dashed', linewidth=1, label="Médiane (50%)")
plt.axvline(moyenne, color='blue', linestyle='dashed', linewidth=1, label="Moyenne")
plt.axvline(moyenne - ecart_type, color='black', linestyle='dashed', linewidth=1, label="Moy - Écart-Type")

plt.xlabel("Score TF-IDF")
plt.ylabel("Nombre de mots")
plt.title("Distribution des scores TF-IDF")
plt.legend()
plt.grid(True)
plt.show()
