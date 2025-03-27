import os
import logging
import xml.etree.ElementTree as ET
from lxml import html
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DOSSIER_BULLETINS = "BULLETINS/"

XPATHS = {
    "numero_bulletin": "//tr[1]/td[3]/p/span[1]",
    "date": "//tr[1]/td[3]/p/span[3]",
    "rubrique": "//tr[3]/td[1]/p[1]/span[1]",
    "titre": "//tr[3]/td[1]/p[1]/span[2]",
    "auteur": "//tr[8]/td[2]/p/span",
    "texte": "//tr[3]/td[1]/p/span | //tr[3]/td[1]/span",
    "images": "//tr[3]/td[1]/div/img",
    "contacts": "//tr[6]/td[2]"
}

def extraire_infos(fichier_html):
    """Extrait les informations d'un fichier HTML avec XPath."""
    try:
        with open(fichier_html, "r", encoding="utf-8") as file:
            tree = html.fromstring(file.read())

        def get_text(xpath, all_text=False):
            elements = tree.xpath(xpath)
            if all_text:
                return "\n".join(e.text_content().strip() for e in elements if e.text_content().strip()) or "Non disponible"
            return elements[0].text_content().strip() if elements else "Inconnu"

        # Extraction des images avec légendes
        images = [{"url": img.get("src", "Inconnu"),
                   "legende": (img.xpath("following-sibling::span/text()") or ["Pas de légende"])[0]}
                  for img in tree.xpath(XPATHS["images"])]

        # Gestion du format de la date
        try:
            date_formattee = datetime.strptime(get_text(XPATHS["date"]), "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            date_formattee = get_text(XPATHS["date"])

        return {
            "numero_bulletin": get_text(XPATHS["numero_bulletin"]),
            "date": date_formattee,
            "rubrique": get_text(XPATHS["rubrique"]),
            "titre": get_text(XPATHS["titre"]),
            "auteur": get_text(XPATHS["auteur"]),
            "texte": get_text(XPATHS["texte"], all_text=True),
            "contacts": get_text(XPATHS["contacts"], all_text=True),
            "images": images
        }

    except Exception as e:
        logging.error(f"Erreur dans {fichier_html}: {e}")
        return None

def generer_xml():
    """Génère un fichier XML à partir des fichiers HTML."""
    if not os.path.exists(DOSSIER_BULLETINS):
        logging.error(f"Le dossier {DOSSIER_BULLETINS} est introuvable.")
        return

    root = ET.Element("corpus")

    for fichier in sorted(os.listdir(DOSSIER_BULLETINS)):
        if fichier.endswith((".htm", ".html")):
            logging.info(f"Traitement : {fichier}")
            infos = extraire_infos(os.path.join(DOSSIER_BULLETINS, fichier))

            if infos:
                bulletin = ET.SubElement(root, "bulletin")

                for key, value in infos.items():
                    if key == "images":
                        images_element = ET.SubElement(bulletin, "images")
                        for img in value:
                            img_element = ET.SubElement(images_element, "image")
                            ET.SubElement(img_element, "urlImage").text = img["url"]
                            ET.SubElement(img_element, "legendeImage").text = img["legende"]
                    else:
                        ET.SubElement(bulletin, key).text = value

    try:
        ET.ElementTree(root).write("corpus.xml", encoding="utf-8", xml_declaration=True)
        logging.info("✅ Fichier XML généré avec succès !")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde du XML : {e}")

if __name__ == "__main__":
    generer_xml()
