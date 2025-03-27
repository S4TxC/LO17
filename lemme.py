import spacy
import xml.etree.ElementTree as ET

# Charger le modèle français de SpaCy
nlp = spacy.load("fr_core_news_sm")

# Fonction pour obtenir les lemmes des mots dans le texte
def get_lemmas_from_text(text):
    doc = nlp(text)
    lemmas = {}
    for token in doc:
        if token.is_stop or token.is_punct:
            continue  # Ignorer les mots vides (stop words) et la ponctuation
        lemmas[token.text] = token.lemma_
    return lemmas

# Fonction pour analyser le fichier XML
def analyze_xml(file_path):
    # Lire et parser le fichier XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Créer un dictionnaire pour stocker les mots et leurs lemmes
    lemmas = {}

    # Parcours de chaque article du fichier XML
    for article in root.findall('bulletin'):  # Adaptez selon la structure de votre XML
        # Récupérer le titre et le texte de l'article
        title = article.find('titre').text if article.find('titre') is not None else ""
        text = article.find('texte').text if article.find('texte') is not None else ""
        
        # Extraire les lemmes du titre et du texte
        title_lemmas = get_lemmas_from_text(title)
        text_lemmas = get_lemmas_from_text(text)
        
        # Ajouter les lemmes au dictionnaire global
        lemmas.update(title_lemmas)
        lemmas.update(text_lemmas)

    # Sauvegarder les résultats dans un fichier texte
    with open("lemmas.txt", "w", encoding="utf-8") as f:
        for word, lemma in lemmas.items():
            f.write(f"{word}\t{lemma}\n")

# Appeler la fonction d'analyse en passant le chemin de votre fichier XML
analyze_xml('corpus_nettoye_definitif.xml')
