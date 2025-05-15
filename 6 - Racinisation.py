import nltk
from nltk.stem.snowball import FrenchStemmer
import xml.etree.ElementTree as ET

stemmer = FrenchStemmer()

def extraire_racine_texte(text):
    mots = text.split()  # Séparer les mots
    stems = {}
    for mot in mots:
        stems[mot] = stemmer.stem(mot)
    return stems

def analyse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    stemming = {}

    for article in root.findall('bulletin'):
        tokenize = article.find('tokenisation').text if article.find('tokenisation') is not None else ""

        tokenize_stems = extraire_racine_texte(tokenize)

        stemming.update(tokenize_stems)

    with open("TxtFiles/StemmingSnowball.txt", "w", encoding="utf-8") as f:
        for word, stem in stemming.items():
            f.write(f"{word}\t{stem}\n")

analyse_xml('corpus2.xml')
