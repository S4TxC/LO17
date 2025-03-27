import xml.etree.ElementTree as ET
import re
import sys
import os

def segmenter_fichier_xml(fichier_xml, fichier_sortie):
    # Parse du fichier XML
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    
    with open(fichier_sortie, 'w', encoding="utf-8") as sortie:
        # Parcours de chaque bulletin dans le corpus
        for bulletin in root.findall("bulletin"):
            # Extraire le nom du fichier depuis l'élément <fichier>
            fichier_nom = bulletin.find("fichier").text

            titre = bulletin.find("titre").text
            texte = bulletin.find("texte").text

            # Si le titre ou le texte existe, on les découpe en tokens
            for contenu in [titre, texte]:
                if contenu:
                    # Nettoyer et découper en tokens : enlever la ponctuation et découper en mots
                    tokens = re.findall(r'\b\w+\b', contenu.lower())  # On garde seulement les mots alphanumériques
                    for token in tokens:
                        # Écrire dans le fichier de sortie avec le nom du fichier
                        sortie.write(f"{token}\t{fichier_nom}\n")

# Vérification des arguments en ligne de commande
if len(sys.argv) != 3:
    print("Erreur syntaxe, manque arguments suivre syntaxe: python Segmente.py <fichier_xml> <fichier_sortie>")
    sys.exit(1)

# Récupération des fichiers en arguments
fichier_xml = sys.argv[1]
fichier_sortie = sys.argv[2]

# Appel de la fonction avec les fichiers spécifiés
segmenter_fichier_xml(fichier_xml, fichier_sortie)
