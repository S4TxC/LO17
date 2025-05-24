# Projet LO17 - Indexation et Recherche d’information

## Objectifs

L'objectif principal de ce projet est de réaliser un système d’indexation et de recherche d’informations sur un ensemble d'articles provenant du site de l'ADIT. Ce système permettra de répondre à des requêtes spécifiques basées sur des articles de veille technologique et scientifique publiés entre 2011 et 2014.

### Objectifs détaillés :

- Création d'un corpus à partir des fichiers HTML fournis.
- Gestion des mots vides pour améliorer la pertinence des recherches.
- Indexation du corpus selon un paradigme (lemme vs racines).
- Implémentation d'un correcteur orthographique et gestion de ses limites.
- Traitement du langage naturel pour l’indexation et la recherche d’information.
- Développement du moteur de recherche pour répondre à des requêtes spécifiques.

## Organisation du repo

Le dossier ***BULLETINS*** contient la base de données des articles de l'ADIT au format HTML.

Le dossier ***Corpus*** contient les différentes versions du corpus.

Le dossier ***index_inverses*** contient les index inversés générés pour effectuer la recherche dans le moteur.

Le dossier ***TD*** contient les sujets des TD liés au projet.

Le dossier ***TxtFiles*** contient les fichiers texte utilisés pour le traitement.

## Fichiers python

**Analyse_TF_IDF.py** : Script permettant d'effectuer l’analyse TF-IDF sur le corpus.

**CorrecteurOrthographique.py** : Implémentation d'un correcteur orthographique.

**CreateSubFile.py** : Script intermédiaire pour faire les substitutions dans la partie tokenisation.

**IndexInverse.py** : Permet la création de l'index inverse.

**Interface.py** : Interface Gradio utilisateur pour interagir avec le système de recherche.

**Lemmatisation.py** : Script pour effectuer la lemmatisation des mots dans le corpus.

**Moteur.py** : Le moteur de recherche.

**NettoieXML.py** : Permet de nettoyer les données XML extraites des fichiers HTML.

**Performances.py** : Analyse des performances du moteur de recherche (temps de réponse, pertinence).

**Racinisation.py** : Implémentation de la racinisation des mots dans le corpus.

**Segmente.py** : Segmentation du texte en tokens.

**Stopwords.py** : Gestion des mots vides dans le processus de recherche et d’indexation.

**StatsLR.py** : Calcul des statistiques comparatives entre lemmes et racines.

**Traitement_requete.py** : Traitement des requêtes de recherche de l'utilisateur.

## Pour tester l'ENSEMBLE du code (sinon tester juste le moteur, les performances et l'interface)

- Cloner le repo

- Supprimer les fichiers des dossiers TxtFiles, Corpus et index_inverses

- Lancer dans l'ordre les scripts : 

```bash
python Script.py
python Segmente.py
python TF_IDF.py
python Analyse_TF_IDF.py
python Stopwords.py
python CreateSubFile.py
python Substitute.py
python NettoieXML.py
python ScriptXMLNettoye.py
python Lemmatisation.py
python Racinisation.py
python StatsLR.py
python IndexInverse.py
python CorrecteurOrthographique.py
python Traitement_requete.py
python Moteur.py
python Performances.py
python Interface.py
```

- Sinon simplement lancer : 
```bash
python Interface.py
```
et suivre l'adresse localhost fournie pour lancer l'interface Gradio.