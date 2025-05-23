                ####### Fichier pour segmenter tous les termes du corpus #######

import xml.etree.ElementTree as ET
import re

def segmenter_fichier_xml():
    fichier_xml = "Corpus/corpusV2.xml"
    fichier_sortie = "TxtFiles/segmente.txt"

    tree = ET.parse(fichier_xml)                                                        
    root = tree.getroot()
    
    with open(fichier_sortie, 'w', encoding="utf-8") as sortie:
        for bulletin in root.findall("bulletin"):
            fichier_nom = bulletin.find("fichier").text                             # Extraire le nom du fichier depuis l'élément <fichier>
            texte = bulletin.find("texte").text
            if texte:
                tokens = re.findall(r"\b\w+\b", re.sub(r"([ldjmnstcq])'", r"\1' ", texte.lower()))
                for token in tokens:
                    sortie.write(f"{token}\t{fichier_nom}\n")

if __name__ == "__main__":
    segmenter_fichier_xml()