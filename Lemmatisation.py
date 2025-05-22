###########################################################################################################

############################### Fichier lemmatisation du corpus avec SpaCy  ###############################

###########################################################################################################

import spacy
import xml.etree.ElementTree as ET

nlp = spacy.load("fr_core_news_sm")                                           # Installer fr_core_news_sm : python -m spacy download fr_core_news_sm

def extraire_lemmes_texte(text):
    doc = nlp(text)
    lemmas = {}
    for token in doc:
        if token.is_stop or token.is_punct:
            continue                                                          # Ignorer les stop words et la ponctuation
        lemmas[token.text] = token.lemma_
    return lemmas

def analyse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    lemmatisation = {}

    for article in root.findall('bulletin'):
        tokenize = article.find('tokenisation').text if article.find('tokenisation') is not None else ""
        tokenize_lemmas = extraire_lemmes_texte(tokenize)
        lemmatisation.update(tokenize_lemmas)

    with open("TxtFiles/LemmatisationSpaCy.txt", "w", encoding="utf-8") as f:
        for word, lemma in lemmatisation.items():
            f.write(f"{word}\t{lemma}\n")

analyse_xml('corpus2.xml')