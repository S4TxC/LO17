import plotly.graph_objects as go
from collections import Counter
import spacy

nlp = spacy.load("fr_core_news_sm")

def stats(file_path_lemma, file_path_stem):
    with open(file_path_lemma, "r", encoding="utf-8") as f:
        lemmes = [line.split()[1] for line in f.readlines()]
        
    with open(file_path_stem, "r", encoding="utf-8") as f:
        stems = [line.split()[1] for line in f.readlines()]
    
    lemmes_count = Counter(lemmes)
    stems_count = Counter(stems)
    
    pos_tags_lemme = [token.pos_ for token in nlp(" ".join(lemmes))]
    pos_tags_stem = [token.pos_ for token in nlp(" ".join(stems))]
    
    pos_count_lemme = Counter(pos_tags_lemme)
    pos_count_stem = Counter(pos_tags_stem)
    
    # Graphique des tags POS 
    pos_labels = list(set(list(pos_count_lemme.keys()) + list(pos_count_stem.keys())))
    pos_values_lemme = [pos_count_lemme.get(label, 0) for label in pos_labels]
    pos_values_stem = [pos_count_stem.get(label, 0) for label in pos_labels]
    
    fig_pos = go.Figure(data=[go.Bar(x=pos_labels, y=pos_values_lemme, name='Lemmatisation', marker_color='skyblue'), go.Bar(x=pos_labels, y=pos_values_stem, name='Racinisation', marker_color='lightcoral')])
    fig_pos.update_layout(title="Répartition des catégories grammaticales (POS tags) - Lemmatisation vs Racinisation", xaxis_title="Catégories grammaticales", yaxis_title="Fréquence", barmode='group', xaxis_tickangle=-45, template="plotly_white")
    fig_pos.show()
    
    # Graphique des fréquences des mots
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=list(lemmes_count.values()), name='Lemmatisation', marker_color='skyblue'))
    fig.add_trace(go.Histogram(x=list(stems_count.values()), name='Racinisation', marker_color='lightcoral'))
    fig.update_layout(title="Distribution des fréquences des lemmes/racines - Lemmatisation vs Racinisation", xaxis_title="Fréquence", yaxis_title="Nombre de mots", template="plotly_white")
    fig.show()

stats("TxtFiles/LemmatisationSpaCy.txt", "TxtFiles/RacinisationNLTK.txt")
