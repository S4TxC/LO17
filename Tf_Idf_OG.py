import math
from collections import Counter, defaultdict

fichier_tokens = "test.txt"
fichier_tf = "X1 - tf.txt"
fichier_idf = "X2 - idf.txt"
fichier_tf_idf = "X3 - tf_idf.txt"


# Étape 1 : Lire tokens_sortie.txt et compter le TF

tf_dict = defaultdict(Counter)  # {doc: {mot: count}}
df_dict = Counter()  # {mot: nombre de documents contenant ce mot}
documents = set()  # Pour compter le nombre total de documents

with open(fichier_tokens, 'r', encoding='utf-8') as f:
    for ligne in f:
        mot, doc = ligne.strip().split('\t')
        tf_dict[doc][mot] += 1
        documents.add(doc)

N = len(documents)


# Étape 2 : Calculer DF (nombre de documents contenant chaque mot)

for doc, mots in tf_dict.items():
    for mot in mots:
        df_dict[mot] += 1


# Étape 3 : Calculer TF et IDF

idf_dict = {mot: math.log10(N / df_t) for mot, df_t in df_dict.items()}


# Étape 4 : Écrire les fichiers de sortie

with open(fichier_tf, 'w', encoding='utf-8') as f_tf, \
     open(fichier_idf, 'w', encoding='utf-8') as f_idf, \
     open(fichier_tf_idf, 'w', encoding='utf-8') as f_tf_idf:

    # Écriture du TF
    for doc, mots in tf_dict.items():
        total_mots = sum(mots.values())  # Nombre total de mots dans le doc
        for mot, count in mots.items():
            tf = count / total_mots
            f_tf.write(f"{doc}\t{mot}\t{tf}\n")

    # Écriture du IDF
    for mot, idf in idf_dict.items():
        f_idf.write(f"{mot}\t{idf}\n")

    # Écriture du TF-IDF
    for doc, mots in tf_dict.items():
        total_mots = sum(mots.values())
        for mot, count in mots.items():
            tf = count / total_mots
            tf_idf = tf * idf_dict[mot]
            f_tf_idf.write(f"{doc}\t{mot}\t{tf_idf}\n")
