###########################################################################################################

############################### Fichier lemmatisation du corpus avec SpaCy  ###############################

###########################################################################################################


import spacy
import xml.etree.ElementTree as ET

nlp = spacy.load("fr_core_news_sm")                                           # Installer fr_core_news_sm : python -m spacy download fr_core_news_sm

def get_lemmas_from_text(text):
    doc = nlp(text)
    lemmas = {}
    for token in doc:
        if token.is_stop or token.is_punct:
            continue                                                          # Ignorer les stop words et la ponctuation
        lemmas[token.text] = token.lemma_
    return lemmas


def analyze_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    lemmatisation = {}

    for article in root.findall('bulletin'):
        title = article.find('titre').text if article.find('titre') is not None else ""
        text = article.find('texte').text if article.find('texte') is not None else ""
        
        title_lemmas = get_lemmas_from_text(title)
        text_lemmas = get_lemmas_from_text(text)
        
        # Ajouter les lemmes au dictionnaire global
        lemmatisation.update(title_lemmas)
        lemmatisation.update(text_lemmas)

    with open("LemmatisationSpaCy.txt", "w", encoding="utf-8") as f:
        for word, lemma in lemmatisation.items():
            f.write(f"{word}\t{lemma}\n")

analyze_xml('corpus_nettoye_definitif.xml')