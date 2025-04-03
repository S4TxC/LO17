import nltk
from nltk.stem.snowball import FrenchStemmer
import xml.etree.ElementTree as ET

stemmer = FrenchStemmer()

def get_stems_from_text(text):
    words = text.split()  # Séparer les mots
    stems = {}
    for word in words:
        stems[word] = stemmer.stem(word)
    return stems

def analyze_xml_snowball(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    stemming = {}

    for article in root.findall('bulletin'):
        tokenize = article.find('tokenisation').text if article.find('tokenisation') is not None else ""

        tokenize_stems = get_stems_from_text(tokenize)

        stemming.update(tokenize_stems)

    with open("StemmingSnowball.txt", "w", encoding="utf-8") as f:
        for word, stem in stemming.items():
            f.write(f"{word}\t{stem}\n")

analyze_xml_snowball('corpus_nettoye_definitif.xml')
