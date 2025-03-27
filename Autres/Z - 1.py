import os
import logging
import xml.etree.ElementTree as ET
from lxml import html
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dossiers
DOSSIER_BULLETINS = "BULLETINS/"
DOSSIER_IMAGES = "BULLETINS/IMAGESWEB"

# XPaths pour l'extraction
XPATHS = {
    "identifiant": "//tr[6]/td[3]/p/a/span",
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
    try:
        with open(fichier_html, "r", encoding="utf-8") as file:
            contenu = file.read()

        tree = html.fromstring(contenu)
        
        def get_text(xpath):
            element = tree.xpath(xpath)
            return element[0].text_content().strip() if element else "Inconnu"

        def get_all_text(xpath):
            elements = tree.xpath(xpath)
            return "\n".join(e.text_content().strip() for e in elements if e.text_content().strip())

        def get_images():
            images = []
            for img in tree.xpath(XPATHS["images"]):
                src = img.get("src", "Inconnu")
                legende = img.xpath("following-sibling::span/text()")
                images.append({"url": src, "legende": legende[0] if legende else "Pas de légende"})
            return images

        date_brut = get_text(XPATHS["date"])
        date_formattee = datetime.strptime(date_brut, "%d/%m/%Y").strftime("%d/%m/%Y") if date_brut != "Inconnu" else date_brut

        return {
            "identifiant": get_text(XPATHS["identifiant"]),
            "numero_bulletin": get_text(XPATHS["numero_bulletin"]),
            "date": date_formattee,
            "rubrique": get_text(XPATHS["rubrique"]),
            "titre": get_text(XPATHS["titre"]),
            "auteur": get_text(XPATHS["auteur"]),
            "texte": get_all_text(XPATHS["texte"]) or "Pas de texte",
            "images": get_images(),
            "contacts": get_all_text(XPATHS["contacts"]) or "Pas de contact"
        }

    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de {fichier_html}: {e}")
        return None

def generer_xml():
    root = ET.Element("corpus")

    if not os.path.exists(DOSSIER_BULLETINS):
        logger.error(f"Le dossier {DOSSIER_BULLETINS} est introuvable.")
        return

    bulletins_traites = 0
    for fichier in sorted(os.listdir(DOSSIER_BULLETINS)):
        if not fichier.endswith((".htm", ".html")):
            continue

        chemin_fichier = os.path.join(DOSSIER_BULLETINS, fichier)
        logger.info(f"Traitement : {fichier}")
        
        infos = extraire_infos(chemin_fichier)
        if not infos:
            continue

        bulletin = ET.SubElement(root, "bulletin")
        ET.SubElement(bulletin, "fichier").text = fichier
        ET.SubElement(bulletin, "numero").text = infos["numero_bulletin"]
        ET.SubElement(bulletin, "date").text = infos["date"]
        ET.SubElement(bulletin, "rubrique").text = infos["rubrique"]
        ET.SubElement(bulletin, "titre").text = infos["titre"]
        ET.SubElement(bulletin, "auteur").text = infos["auteur"]
        ET.SubElement(bulletin, "texte").text = infos["texte"]

        images_element = ET.SubElement(bulletin, "images")
        for img in infos["images"]:
            img_element = ET.SubElement(images_element, "image")
            ET.SubElement(img_element, "urlImage").text = img["url"]
            ET.SubElement(img_element, "legendeImage").text = img["legende"]

        ET.SubElement(bulletin, "contact").text = infos["contacts"]

        bulletins_traites += 1

    tree = ET.ElementTree(root)
    chemin_xml = "corpus.xml"
    tree.write(chemin_xml, encoding="utf-8", xml_declaration=True)

    logger.info(f"✅ {bulletins_traites} bulletins traités. Fichier XML généré: {chemin_xml}")

if __name__ == "__main__":
    generer_xml()