import spacy

nlp = spacy.load("fr_core_news_sm")

def charger_lexique(fichier):
    lexique = {}
    with open(fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            mot, lemme = ligne.strip().split('\t')
            lexique[mot.lower()] = lemme.lower()
    return lexique

def lemmatiser_phrase(phrase, lexique):
    doc = nlp(phrase)
    resultats = {}

    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        lemma_spacy = token.lemma_.lower() 
        resultats[token.text.lower()] = lexique.get(lemma_spacy, lemma_spacy)  

    return resultats

lexique = charger_lexique("TxtFiles/LemmatisationSpaCy.txt")

phrase = input("Entrez une phrase : ").strip()
lemmes = lemmatiser_phrase(phrase, lexique)

print("\nRésultat :")
for mot, lemme in lemmes.items():
    print(f"{mot} -> {lemme}")
