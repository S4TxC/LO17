import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from Moteur import rechercher_documents
import time

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

def calcul_precision_rappel(requete, docs_retournes):
    ret = {str(d) for d in docs_retournes}
    pertinents = documents_pertinents.get(requete, set())
    intersection = ret & pertinents
    precision = len(intersection) / len(ret) if ret else 0
    rappel = len(intersection) / len(pertinents) if pertinents else 0
    return precision, rappel

def mesurer_temps_moyen(requete, repetitions=10):
    start = time.time()
    for _ in range(repetitions):
        _ = rechercher_documents(requete)
    end = time.time()
    return (end - start) / repetitions

def recherche_et_stats(req_selectionnee):
    documents = rechercher_documents(req_selectionnee)
    p, r = calcul_precision_rappel(req_selectionnee, documents)
    tps = mesurer_temps_moyen(req_selectionnee)
    stats = f"""
### Statistiques
- Précision : {p:.2f}
- Rappel : {r:.2f}
- Temps moyen : {tps:.3f} s

### Documents trouvés ({len(documents)} résultats) :
""" + "\n".join(documents)
    return stats

def evaluation_globale():
    precisions, rappels, temps_reponses = [], [], []

    for req in requêtes:
        docs = rechercher_documents(req)
        p, r = calcul_precision_rappel(req, docs)
        precisions.append(p)
        rappels.append(r)
        temps_reponses.append(mesurer_temps_moyen(req))

    df = pd.DataFrame({
        "Requête": requêtes,
        "Précision": precisions,
        "Rappel": rappels,
        "Temps de réponse (s)": temps_reponses
    })

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=requêtes, y=precisions, mode="lines+markers", name="Précision"))
    fig1.add_trace(go.Scatter(x=requêtes, y=rappels, mode="lines+markers", name="Rappel"))
    fig1.update_layout(title="Précision et Rappel", xaxis_title="Requêtes", yaxis_title="Valeur", xaxis_tickangle=45)

    fig2 = go.Figure(go.Bar(x=requêtes, y=temps_reponses, marker_color='orange'))
    fig2.update_layout(title="Temps de réponse moyen", xaxis_title="Requêtes", yaxis_title="Temps (s)", xaxis_tickangle=45)

    return df, fig1, fig2

with gr.Blocks(title="Moteur de Recherche LO17") as demo:
    gr.Markdown("# Interface Moteur de Recherche LO17")

    with gr.Tab("Évaluation"):
        gr.Markdown("## Sélectionne une requête pour tester le moteur :")
        requete_choisie = gr.Dropdown(choices=requêtes, label="Requête prédéfinie")
        resultat_indiv = gr.Markdown()
        bouton_test = gr.Button("Lancer la recherche sur cette requête")
        bouton_test.click(fn=recherche_et_stats, inputs=requete_choisie, outputs=resultat_indiv)

        gr.Markdown("## Lancer l'évaluation complète")
        bouton_eval = gr.Button("Évaluer toutes les requêtes")
        tableau = gr.Dataframe(label="Résultats de l'évaluation")
        graphe1 = gr.Plot(label="Graphique précision / rappel")
        graphe2 = gr.Plot(label="Graphique temps de réponse")
        bouton_eval.click(fn=evaluation_globale, inputs=[], outputs=[tableau, graphe1, graphe2])

demo.launch()
