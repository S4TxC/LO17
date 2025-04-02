##############################################################################################

############################### Fichier pour générer le corpus ###############################

##############################################################################################


import os
import xml.etree.ElementTree as ET
from lxml import html
import re
from datetime import datetime

DOSSIER_BULLETINS = "BULLETINS/"
DOSSIER_IMAGES = "BULLETINS/IMAGESWEB"


# Patterns XPaths pour extraire les infos qu'on veut
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
            tree = html.fromstring(file.read())

        def get_text(xpath):
            element = tree.xpath(xpath)
            if len(element) > 0:
                return element[0].text_content().strip()
            else:
                return "Inconnu"

        def get_all_text(xpath):
            elements = tree.xpath(xpath)
            textes = []
            for e in elements:
                texte = e.text_content().strip()
                if texte:
                    textes.append(texte)
            
            if textes:
                texte_final = "\n".join(textes)
                
                rubrique = get_text(XPATHS["rubrique"])
                titre = get_text(XPATHS["titre"])

                if texte_final.startswith(rubrique):
                    texte_final = texte_final[len(rubrique):].strip()
                if texte_final.startswith(titre):
                    texte_final = texte_final[len(titre):].strip()

                texte_final = re.sub(r"http://www\.bulletins-electroniques\.com/actualites/\d+\.htm", "", texte_final).strip()
                
                return texte_final
            
            return "Pas de texte"

        
        def extraire_contacts(xpath):
            elements = tree.xpath(xpath)
            contacts_textes = []
    
            for e in elements:
                texte = e.text_content().strip()
                if texte:
                    contacts_textes.append(texte)

            return "\n".join(contacts_textes).strip() if contacts_textes else "Pas de contact"


        def get_images():
            images = []
            elements = tree.xpath(XPATHS["images"])
            for img in elements:
                src = img.get("src", "Inconnu")
                legende_elements = img.xpath("following-sibling::span/strong/text()") # following-sibling : Pour récupérer directement l'élément suivant suivant le pattern indiqué, ajouter "| following-sibling::span/text()") si on veut récupérer les crédits 
                if len(legende_elements) > 0:
                    legende = legende_elements[0]
                else:
                    legende = "Pas de légende"
                images.append({"url": src, "legende": legende})
            return images

        date_brut = get_text(XPATHS["date"])
        try:
            date_formattee = datetime.strptime(date_brut, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            date_formattee = date_brut

        return {
            "identifiant": get_text(XPATHS["identifiant"]),
            "numero_bulletin": get_text(XPATHS["numero_bulletin"]),
            "date": date_formattee,
            "rubrique": get_text(XPATHS["rubrique"]),
            "titre": get_text(XPATHS["titre"]),
            "auteur": get_text(XPATHS["auteur"]),
            "texte": get_all_text(XPATHS["texte"]),
            "images": get_images(),
            "contacts": extraire_contacts(XPATHS["contacts"])
        }

    except Exception:
        return None

def generer_xml():
    root = ET.Element("corpus")

    if not os.path.exists(DOSSIER_BULLETINS):
        return

    for fichier in sorted(os.listdir(DOSSIER_BULLETINS)):
        if fichier.endswith(".htm") or fichier.endswith(".html"):
            chemin_fichier = os.path.join(DOSSIER_BULLETINS, fichier)
            infos = extraire_infos(chemin_fichier)

            if infos is not None:
                bulletin = ET.SubElement(root, "bulletin")
                ET.SubElement(bulletin, "fichier").text = re.sub(r"\.html?$", "", fichier) #fichier
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

    ET.ElementTree(root).write("corpus.xml", encoding="utf-8", xml_declaration=True)


def nettoyer_texte(texte):
    if texte is None:
        return ""

    texte = re.sub(r'ADIT\s*-\s*', '', texte)  # Supprime "ADIT -"
    texte = re.sub(r'\s*-?\s*email\s*:\s*\S+@\S+', '', texte)  # Supprime les emails
    texte = re.sub(r'\bBE France\s*', '', texte)  # Supprime "BE France"
    return texte.strip()


def nettoyer_xml(fichier_entree, fichier_sortie):
    tree = ET.parse(fichier_entree)
    root = tree.getroot()

    for bulletin in root.findall("bulletin"):
        numero = bulletin.find("numero")
        auteur = bulletin.find("auteur")

        if numero is not None:
            numero.text = nettoyer_texte(numero.text)

        if auteur is not None:
            auteur.text = nettoyer_texte(auteur.text)

    tree.write(fichier_sortie, encoding="utf-8", xml_declaration=True)
    print(f"Fichier nettoyé et enregistré sous : {fichier_sortie}")


if __name__ == "__main__":
    generer_xml()
    nettoyer_xml("corpus.xml", "corpus_nettoye.xml")