import os
import math
from collections import Counter

def calculer_tf(repertoire_documents):
    tf_dict = {}
    for nom_fichier in os.listdir(repertoire_documents):
        chemin_fichier = os.path.join(repertoire_documents, nom_fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            texte = fichier.read()
            mots = texte.split()
            total_mots = len(mots)
            compteur_mots = Counter(mots)
            for mot, count in compteur_mots.items():
                tf = count / total_mots
                tf_dict[(nom_fichier, mot)] = tf
    return tf_dict

def calculer_idf(repertoire_documents):
    N = len(os.listdir(repertoire_documents))
    df = Counter()
    for nom_fichier in os.listdir(repertoire_documents):
        chemin_fichier = os.path.join(repertoire_documents, nom_fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            mots_uniques = set(fichier.read().split())
            for mot in mots_uniques:
                df[mot] += 1
    idf_dict = {mot: math.log10(N / df_t) for mot, df_t in df.items()}
    return idf_dict

def calculer_tf_idf(tf_dict, idf_dict):
    tf_idf_dict = {}
    for (nom_fichier, mot), tf in tf_dict.items():
        idf = idf_dict.get(mot, 0)
        tf_idf = tf * idf
        tf_idf_dict[(nom_fichier, mot)] = tf_idf
    return tf_idf_dict

repertoire_documents = 'C:\Users\y455\Desktop\LO17'
tf = calculer_tf(repertoire_documents)
idf = calculer_idf(repertoire_documents)
tf_idf = calculer_tf_idf(tf, idf)

with open('tf.txt', 'w', encoding='utf-8') as f_tf, \
     open('idf.txt', 'w', encoding='utf-8') as f_idf, \
     open('tf_idf.txt', 'w', encoding='utf-8') as f_tf_idf:
    for (doc, mot), valeur in tf.items():
        f_tf.write(f"{doc}\t{mot}\t{valeur}\n")
    for mot, valeur in idf.items():
        f_idf.write(f"{mot}\t{valeur}\n")
    for (doc, mot), valeur in tf_idf.items():
        f_tf_idf.write(f"{doc}\t{mot}\t{valeur}\n")
