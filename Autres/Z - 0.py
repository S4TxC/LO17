import os
import re
import html
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Chemins des dossiers
DOSSIER_BULLETINS = "BULLETINS/"
DOSSIER_IMAGES = "BULLETINS/IMAGESWEB"

def extraire_infos_depuis_html(fichier_html):
    """Extrait la date, le numéro du bulletin et le titre de l'article."""
    try:
        with open(fichier_html, "r", encoding="utf-8") as file:
            contenu = file.read()

        # Recherche des informations dans la balise title
        pattern = r"<title>(\d{4}/\d{2}/\d{2})&nbsp;&gt; BE France&nbsp;(\d+)&nbsp;&gt; (.+?)</title>"
        match = re.search(pattern, contenu)

        if match:
            date_str = match.group(1)
            # Conversion au format jj/mm/aaaa
            try:
                date_obj = datetime.strptime(date_str, "%Y/%m/%d")
                date_formattee = date_obj.strftime("%d/%m/%Y")
            except ValueError:
                date_formattee = date_str  # Garde le format original en cas d'erreur

            return {
                "date": date_formattee,
                "numero_bulletin": match.group(2),
                "titre": html.unescape(match.group(3))
            }
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des informations de base pour {fichier_html}: {e}")
    
    return None

def extraction_auteur_depuis_html(fichier_html):
    """Extrait l'auteur de l'article."""
    try:
        with open(fichier_html, "r", encoding="utf-8") as file:
            contenu = file.read()

        # Utilisation de BeautifulSoup pour une extraction plus fiable
        soup = BeautifulSoup(contenu, "html.parser")
        texte_avec_auteur = soup.find(string=lambda text: text and "ADIT -" in text)
        
        if texte_avec_auteur:
            match = re.search(r"ADIT - (.*?) - email", texte_avec_auteur)
            if match:
                return html.unescape(match.group(1)).strip()
            
        # Méthode de secours avec regex directe
        match = re.search(r"ADIT - (.*?) - email", contenu)
        if match:
            return html.unescape(match.group(1)).strip()
            
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de l'auteur pour {fichier_html}: {e}")
    
    return "Inconnu"

def extraction_rubrique_depuis_html(fichier_html):
    """Extrait la rubrique de l'article."""
    try:
        with open(fichier_html, "r", encoding="utf-8") as file:
            contenu = file.read()

        soup = BeautifulSoup(contenu, "html.parser")
        
        # Recherche dans les cellules avec la classe FWExtra2
        cell = soup.find("td", class_="FWExtra2")
        if cell and cell.find("span"):
            texte_rubrique = cell.find("span").get_text(strip=True).split('\n')[0]
            return texte_rubrique.strip()
            
        # Méthode de secours avec regex
        match = re.search(r'<td.*?class="FWExtra2">\s*<p.*?><span.*?>(.*?)<br>', contenu, re.DOTALL)
        if match:
            return html.unescape(match.group(1)).strip()
            
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de la rubrique pour {fichier_html}: {e}")
    
    return "Inconnu"

def extraction_texte_article(fichier_html):
    """Extrait le texte de l'article et le nettoie."""
    try:
        with open(fichier_html, "r", encoding="utf-8") as file:
            contenu = file.read()

        soup = BeautifulSoup(contenu, "html.parser")
        
        # Recherche du contenu principal
        contenu_principal = soup.find("p", class_="style96")
        if contenu_principal and contenu_principal.find("span", class_="style95"):
            texte = contenu_principal.find("span", class_="style95").get_text(strip=True)
            return texte
        
        # Méthode de secours avec regex
        match = re.search(r'<p class="style96"><span class="style95">(.*?)</span></p></td>', contenu, re.DOTALL)
        if match:
            texte = html.unescape(match.group(1))
            texte = re.sub(r'<.*?>', ' ', texte)  # Supprime les balises HTML
            texte = re.sub(r'\s+', ' ', texte)    # Normalise les espaces
            return texte.strip()
            
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction du texte pour {fichier_html}: {e}")
    
    return "Pas de texte disponible"

def verifier_et_extraire_images(chemin_fichier_html):
    """Vérifie si un article possède des images et extrait leurs informations."""
    images_info = []
    
    try:
        numero_article = os.path.splitext(os.path.basename(chemin_fichier_html))[0]
        
        # Vérification que le dossier images existe
        if not os.path.exists(DOSSIER_IMAGES):
            logger.warning(f"Le dossier d'images {DOSSIER_IMAGES} n'existe pas")
            return images_info
            
        images_associees = [img for img in os.listdir(DOSSIER_IMAGES) if img.startswith(numero_article)]
        
        if not images_associees:
            return images_info

        with open(chemin_fichier_html, "r", encoding="utf-8") as file:
            contenu = file.read()
        
        soup = BeautifulSoup(contenu, "html.parser")
        
        for img_tag in soup.find_all("img"):
            if not img_tag.has_attr("src"):
                continue
                
            url_image = img_tag["src"]
            if not any(img_file in url_image for img_file in images_associees):
                continue

            # Recherche de la légende (peut être dans un span de classe style21 proche)
            legende = "Pas de légende"
            legende_tag = img_tag.find_next("span", class_="style21")
            if legende_tag:
                legende = legende_tag.get_text(strip=True)
            
            images_info.append({"url": url_image, "legende": html.unescape(legende)})
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des images pour {chemin_fichier_html}: {e}")
    
    return images_info

def extraction_contacts(fichier_html):
    """Extrait les contacts de l'article."""
    try:
        with open(fichier_html, "r", encoding="utf-8") as file:
            contenu = file.read()

        soup = BeautifulSoup(contenu, "html.parser")
        
        # Recherche des paragraphes avec classe style44 et span style85
        contacts = []
        for p_tag in soup.find_all("p", class_="style44"):
            span_tag = p_tag.find("span", class_="style85")
            if span_tag:
                # Récupération du texte brut (sans les balises a)
                contact_text = span_tag.get_text(strip=True)
                contacts.append(contact_text)
        
        if contacts:
            return contacts
            
        # Méthode de secours avec regex
        pattern = r'<p class="style44"><span class="style85">(.*?)</a></span></p></td>'
        matches = re.findall(pattern, contenu, re.DOTALL)
        if matches:
            return [re.sub(r'<a.*?>', '', html.unescape(match)).strip() for match in matches]
            
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des contacts pour {fichier_html}: {e}")
    
    return ["Pas de contact disponible"]

def prettify_xml(elem):
    """Indente correctement le XML pour un affichage propre."""
    rough_string = ET.tostring(elem, 'utf-8')
    try:
        import xml.dom.minidom
        reparsed = xml.dom.minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    except Exception:
        logger.warning("Impossible d'utiliser minidom pour formater le XML. Utilisation du format standard.")
        return rough_string.decode('utf-8')

def generer_xml():
    """Génère un fichier XML contenant tous les bulletins selon la structure demandée."""
    root = ET.Element("corpus")
    bulletins_traites = 0
    bulletins_ignores = 0

    # Vérification que le dossier bulletins existe
    if not os.path.exists(DOSSIER_BULLETINS):
        logger.error(f"Le dossier des bulletins {DOSSIER_BULLETINS} n'existe pas")
        return

    for fichier in sorted(os.listdir(DOSSIER_BULLETINS)):
        if fichier.endswith(".htm") or fichier.endswith(".html"):
            chemin_fichier = os.path.join(DOSSIER_BULLETINS, fichier)
            logger.info(f"Traitement du fichier: {fichier}")

            infos = extraire_infos_depuis_html(chemin_fichier)
            if not infos:
                logger.warning(f"Aucune information valide trouvée pour {fichier}")
                bulletins_ignores += 1
                continue

            # Création de l'élément bulletin
            bulletin = ET.SubElement(root, "bulletin")
            
            # Ajout des éléments enfants avec les informations extraites
            ET.SubElement(bulletin, "fichier").text = fichier
            ET.SubElement(bulletin, "numero").text = infos["numero_bulletin"]
            ET.SubElement(bulletin, "date").text = infos["date"]
            ET.SubElement(bulletin, "rubrique").text = extraction_rubrique_depuis_html(chemin_fichier)
            ET.SubElement(bulletin, "titre").text = infos["titre"]
            ET.SubElement(bulletin, "auteur").text = extraction_auteur_depuis_html(chemin_fichier)
            ET.SubElement(bulletin, "texte").text = extraction_texte_article(chemin_fichier)

            # Traitement des images
            images_element = ET.SubElement(bulletin, "images")
            images_info = verifier_et_extraire_images(chemin_fichier)
            
            for img in images_info:
                img_element = ET.SubElement(images_element, "image")
                ET.SubElement(img_element, "urlImage").text = img["url"]
                ET.SubElement(img_element, "legendeImage").text = img["legende"]

            # Traitement des contacts
            contacts = extraction_contacts(chemin_fichier)
            contacts_element = ET.SubElement(bulletin, "contact")
            if contacts:
                contacts_element.text = "\n".join(contacts)
            else:
                contacts_element.text = "Pas de contact"
                
            bulletins_traites += 1

    # Sauvegarde du fichier XML avec une belle mise en forme
    try:
        pretty_xml = prettify_xml(root)
        with open("corpus.xml", "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(pretty_xml)
        
        logger.info(f"✅ Le fichier 'corpus.xml' a été généré avec succès!")
        logger.info(f"📊 Statistiques: {bulletins_traites} bulletins traités, {bulletins_ignores} bulletins ignorés")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du XML: {e}")

if __name__ == "__main__":
    generer_xml()