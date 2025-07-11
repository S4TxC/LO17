                ####### Fichier pour tester les performances du moteur pour un nombre restreint de requêtes #######

import time
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import sys
from Moteur import rechercher_documents 

precisions = []
rappels = []
temps_reponse = []

requêtes = [
    "Donner les articles qui parlent d’apprentissage et de la rubrique Horizons Enseignement.",
    "Je cherche des articles sur les avions.",
    "Je veux les articles de 2012 qui parlent de l’écologie en France.",
    "Quels sont les articles parus entre le 3 mars 2013 et le 4 mai 2013 évoquant les Etats-Unis ?",
    "Je cherche les articles à propos des fleurs ou des arbres.",
    "Articles contenant des images.",
    "Articles parlant de molécules.",
    "Afficher les articles de la rubrique A lire.",
    "Je voudrais tout les articles provenant de la rubrique événement et contenant le mot congres dans le titre.",
    "Rechercher tous les articles sur le CNRS et l’innovation à partir de 2013."
]

documents_pertinents = {
    requêtes[0]: {"68281", "68888", "70923"},
    requêtes[1]: {"67797", "69542", "70916", "70920", "71617", "71840", "72933", "74167", "74745"},
    requêtes[2]: {"67071", "67387", "69812", "70420", "70745", "71618", "73877", "75458", "75460"},
    requêtes[3]: set(),
    requêtes[4]: {"68273", "76516", "67387", "67391", "68383", "69182", "69816", "71837", "75458"},
    requêtes[5]: {"67794", "67795", "67800", "67937", "67938", "67940", "67941", "68274", "68276", "68280", "68281", "68383", "68390", "68638", "68881", "68882", "68883", "68886", "69177", "69178", "69179", "69183", "69541", "69542", "69811", "69816", "69821", "70161", "70163", "70165", "70420", "70421", "70422", "70423", "70424", "70425", "70744", "70747", "70914", "70916", "71612", "71614", "71621", "71835", "71836", "71837", "72114", "72115", "72119", "72392", "72397", "72629", "72635", "72636", "72932", "72933", "72939", "72940", "73182", "73183", "73185", "73430", "73431", "73683", "73684", "73876", "74167", "74168", "74450", "74752", "75063", "75065", "75457", "75458", "75788", "75789", "75791", "75792", "75797", "76211", "76212", "76213"},
    requêtes[6]: {"67390", "67558", "67800", "68387", "68390", "69539", "70167", "70423", "70425", "70919", "70922", "72115", "72116", "72118", "72394", "72634", "73187", "73433", "73436", "73878", "75065", "75459", "76206", "76511", "76512"},
    requêtes[7]: {"68283", "69821", "70429", "70753", "71366", "71621", "72401", "72940", "74457", "74752", "76213"},
    requêtes[8]: {"72120", "72937", "73882"},
    requêtes[9]: {"72632", "72939", "73683", "74452", "75460"}
}

def calcul_precision_rappel(requete, documents_retournes):
    documents_retournes = {str(doc) for doc in documents_retournes}
    documents_pertinents_requete = {str(doc) for doc in documents_pertinents.get(requete, set())}

    print(f"Documents pertinents pour la requête {requete} : {documents_pertinents_requete}")
    print(f"Documents retournés par le moteur : {documents_retournes}")

    pertinents_retournes = documents_retournes.intersection(documents_pertinents_requete)
    precision = len(pertinents_retournes) / len(documents_retournes) if documents_retournes else 0
    rappel = len(pertinents_retournes) / len(documents_pertinents_requete) if documents_pertinents_requete else 0
    return precision, rappel

def mesurer_temps_moyen(requete, repetitions=100):
    start_time = time.time()
    for _ in range(repetitions):
        documents_retournes = set(rechercher_documents(requete))
    end_time = time.time()
    temps_total = end_time - start_time
    temps_moyen = temps_total / repetitions
    return temps_moyen

for requete in requêtes:
    documents_retournes = set(rechercher_documents(requete))
    precision, rappel = calcul_precision_rappel(requete, documents_retournes)
    precisions.append(precision)
    rappels.append(rappel)
    temps_moyen = mesurer_temps_moyen(requete)
    temps_reponse.append(temps_moyen)

df = pd.DataFrame({"Requête": requêtes, "Précision": precisions, "Rappel": rappels, "Temps de réponse moyen (s)": temps_reponse})

print("\nTableau des résultats :")
print(df)

fig_prec_rappel = go.Figure()
fig_prec_rappel.add_trace(go.Scatter(x=requêtes, y=precisions, mode='lines+markers', name='Précision', line=dict(color='blue', width=2), marker=dict(size=6)))
fig_prec_rappel.add_trace(go.Scatter(x=requêtes, y=rappels, mode='lines+markers', name='Rappel', line=dict(color='green', width=2), marker=dict(size=6)))
fig_prec_rappel.update_layout(title="Précision et Rappel par requête", xaxis_title="Requêtes", yaxis_title="Valeur", showlegend=True)
fig_prec_rappel.show()

fig_temps_reponse = go.Figure(go.Bar(x=requêtes, y=temps_reponse, marker=dict(color='orange'), text=temps_reponse, textposition='auto'))
fig_temps_reponse.update_layout(title="Temps de réponse moyen par requête", xaxis_title="Requêtes", yaxis_title="Temps de réponse moyen (s)", xaxis=dict(tickangle=45))
fig_temps_reponse.show()
