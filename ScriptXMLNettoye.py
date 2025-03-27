import xml.etree.ElementTree as ET

def generer_xml(tokens_file, input_xml, output_xml):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    racine = ET.Element("corpus")

    with open(tokens_file, 'r', encoding='utf-8') as f:
        # Dictionnaire pour stocker les tokens par bulletin (ici on suppose que le bulletin_num est l'identifiant du bulletin)
        # Le format attendu est : token\tbulletin_num
        tokens_par_bulletin = {}

        for ligne in f:
            token, bulletin_num = ligne.strip().split('\t')

            if token != "''":
                if bulletin_num not in tokens_par_bulletin:
                    tokens_par_bulletin[bulletin_num] = []
                tokens_par_bulletin[bulletin_num].append(token)

        for bulletin in root.findall("bulletin"):
            bulletin_num = bulletin.find("fichier").text
            titre = bulletin.find("titre").text
            texte = bulletin.find("texte").text
            rubrique = bulletin.find("rubrique").text
            date = bulletin.find("date").text
            contact = bulletin.find("contact").text

            bulletin_element = ET.SubElement(racine, "bulletin")
            
            fichier_element = ET.SubElement(bulletin_element, "fichier")
            fichier_element.text = bulletin_num
            
            titre_element = ET.SubElement(bulletin_element, "titre")
            titre_element.text = titre

            texte_element = ET.SubElement(bulletin_element, "texte")
            texte_element.text = texte

            rubrique_element = ET.SubElement(bulletin_element, "rubrique")
            rubrique_element.text = rubrique

            date_element = ET.SubElement(bulletin_element, "date")
            date_element.text = date

            contact_element = ET.SubElement(bulletin_element, "contact")
            contact_element.text = contact

            tokens_element = ET.SubElement(bulletin_element, "tokens")
            tokens_element.text = " ".join(tokens_par_bulletin.get(bulletin_num, []))

    tree = ET.ElementTree(racine)
    tree.write(output_xml, encoding="utf-8", xml_declaration=True)

tokens_file = "X7 - Tokens_nettoyes_XML.txt"  # Le fichier de tokens nettoyés
input_xml = "corpus_nettoye.xml"  # Le fichier XML d'entrée avec toutes les informations supplémentaires
output_xml = "corpus_nettoye_definitif.xml"  # Le fichier XML à générer avec les informations complètes

generer_xml(tokens_file, input_xml, output_xml)
