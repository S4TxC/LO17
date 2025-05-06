from collections import Counter
import numpy as np
import spacy
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Charger le modèle SpaCy
nlp = spacy.load("fr_core_news_sm")

def stats(file_path_lemma, file_path_stem):
    # Lecture des lemmes
    with open(file_path_lemma, "r", encoding="utf-8") as f:
        lemmes = [line.split()[1] for line in f.readlines()]
    
    # Lecture des racines
    with open(file_path_stem, "r", encoding="utf-8") as f:
        stems = [line.split()[1] for line in f.readlines()]
    
    # Fréquence des lemmes
    lemma_count = Counter(lemmes)
    # Fréquence des racines
    stem_count = Counter(stems)
    
    # Fréquence des catégories grammaticales pour les lemmes
    pos_tags_lemma = [token.pos_ for token in nlp(" ".join(lemmes))]
    pos_tags_stem = [token.pos_ for token in nlp(" ".join(stems))]
    
    pos_count_lemma = Counter(pos_tags_lemma)
    pos_count_stem = Counter(pos_tags_stem)
    
    # -----------------------------------------
    # 1. Graphique des POS tags comparatif (Lemmatisation vs Racinisation)
    # -----------------------------------------
    pos_labels_lemma = list(pos_count_lemma.keys())
    pos_values_lemma = list(pos_count_lemma.values())
    pos_labels_stem = list(pos_count_stem.keys())
    pos_values_stem = list(pos_count_stem.values())
    
    all_pos_labels = list(set(pos_labels_lemma + pos_labels_stem))              # Assurer que les labels sont les mêmes pour les deux graphiques
    
    # Ajouter 0 pour les POS tags manquants dans un des deux ensembles
    pos_values_lemma = [pos_count_lemma.get(label, 0) for label in all_pos_labels]
    pos_values_stem = [pos_count_stem.get(label, 0) for label in all_pos_labels]
    
    # Création du graphique des POS tags
    fig_pos = go.Figure(data=[
        go.Bar(x=all_pos_labels, y=pos_values_lemma, name='Lemmatisation', marker_color='skyblue'),
        go.Bar(x=all_pos_labels, y=pos_values_stem, name='Racinisation', marker_color='lightcoral')
    ])
    
    fig_pos.update_layout(title="Répartition des catégories grammaticales (POS tags) - Lemmatisation vs Racinisation", xaxis_title="Catégories grammaticales", yaxis_title="Fréquence", barmode='group', xaxis_tickangle=-45, template="plotly_white")
    fig_pos.show()
    
    # -----------------------------------------
    # 2. Graphique des fréquences des mots comparatif (Lemmatisation vs Racinisation)
    # -----------------------------------------
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Distribution des fréquences des lemmes", "Distribution des fréquences des racines"), shared_yaxes=True)
    
    # Données pour les lemmes
    fig.add_trace(go.Histogram(x=list(lemma_count.values()), nbinsx=30, name='Lemmatisation', marker_color='skyblue'), row=1, col=1)
    
    # Données pour les racines
    fig.add_trace(go.Histogram(x=list(stem_count.values()), nbinsx=30, name='Racinisation', marker_color='lightcoral'), row=1, col=2)
    
    fig.update_layout(title="Distribution des fréquences des lemmes/racines - Lemmatisation vs Racinisation",bxaxis_title="Fréquence", yaxis_title="Nombre de mots", template="plotly_white")
    fig.show()

stats("LemmatisationSpaCy.txt", "StemmingSnowball.txt")
