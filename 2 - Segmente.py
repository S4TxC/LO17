################################################################################################################

############################### Fichier pour segmenter tous les termes du corpus ###############################

################################################################################################################


import xml.etree.ElementTree as ET
import re
import sys
import os

def segmenter_fichier_xml(fichier_xml, fichier_sortie):
    tree = ET.parse(fichier_xml)                                                        # Parse du fichier XML
    root = tree.getroot()
    

    with open(fichier_sortie, 'w', encoding="utf-8") as sortie:

        for bulletin in root.findall("bulletin"):                                       # Parcours de chaque bulletin dans le corpus

            fichier_nom = bulletin.find("fichier").text                                 # Extraire le nom du fichier depuis l'élément <fichier>
            titre = bulletin.find("titre").text
            texte = bulletin.find("texte").text

            # Si le titre ou le texte existe, on les découpe en tokens
            for contenu in [titre, texte]:
                if contenu:
                    # Nettoyer et découper en tokens
                    tokens = re.findall(r"\b[\w'-]+\b", contenu.lower())                    # Revoir l'expression ici pour faire une meilleure découpe
                    for token in tokens:
                        sortie.write(f"{token}\t{fichier_nom}\n")


if len(sys.argv) != 3:
    print("Erreur syntaxe, manque arguments suivre syntaxe: python Segmente.py <fichier_xml> <fichier_sortie>")
    sys.exit(1)

fichier_xml = sys.argv[1]
fichier_sortie = sys.argv[2]

segmenter_fichier_xml(fichier_xml, fichier_sortie)
