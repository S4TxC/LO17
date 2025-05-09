##########################################################################################################################

############################### Fichier pour ajouter le traitement des stopwords au corpus ###############################

##########################################################################################################################


import xml.etree.ElementTree as ET

def generer_xml(tokens_file, input_xml, output_xml):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    racine = ET.Element("corpus")

    with open(tokens_file, 'r', encoding='utf-8') as f:
        tokens_par_bulletin = {}

        for ligne in f:
            token, bulletin_num = ligne.strip().split('\t')

            if token != "''":
                if bulletin_num not in tokens_par_bulletin:
                    tokens_par_bulletin[bulletin_num] = []
                tokens_par_bulletin[bulletin_num].append(token)

        for bulletin in root.findall("bulletin"):
            bulletin_num = bulletin.find("fichier").text
            numero = bulletin.find("numero").text
            date = bulletin.find("date").text
            rubrique = bulletin.find("rubrique").text
            titre = bulletin.find("titre").text
            auteur = bulletin.find("auteur").text
            texte = bulletin.find("texte").text
            images = bulletin.find("images")
            contact = bulletin.find("contact").text
            

            bulletin_element = ET.SubElement(racine, "bulletin")
            
            fichier_element = ET.SubElement(bulletin_element, "fichier")
            fichier_element.text = bulletin_num

            numero_element = ET.SubElement(bulletin_element, "numero")
            numero_element.text = numero

            date_element = ET.SubElement(bulletin_element, "date")
            date_element.text = date

            rubrique_element = ET.SubElement(bulletin_element, "rubrique")
            rubrique_element.text = rubrique

            titre_element = ET.SubElement(bulletin_element, "titre")
            titre_element.text = titre

            auteur_element = ET.SubElement(bulletin_element, "auteur")
            auteur_element.text = auteur

            texte_element = ET.SubElement(bulletin_element, "texte")
            texte_element.text = texte 

            tokens_element = ET.SubElement(bulletin_element, "tokenisation")
            tokens_element.text = " ".join(tokens_par_bulletin.get(bulletin_num, []))

            if images is not None:
                images_element = ET.SubElement(bulletin_element, "images")

                for image in images.findall("image"):
                    image_element = ET.SubElement(images_element, "image")
                    
                    url_element = image.find("urlImage")
                    legende_element = image.find("legendeImage")

                    if url_element is not None:
                        ET.SubElement(image_element, "urlImage").text = url_element.text
                    if legende_element is not None:
                        ET.SubElement(image_element, "legendeImage").text = legende_element.text

            contact_element = ET.SubElement(bulletin_element, "contact")
            contact_element.text = contact


    tree = ET.ElementTree(racine)
    tree.write(output_xml, encoding="utf-8", xml_declaration=True)

tokens_file = "TokenN2.txt"                                 #"X7 - Tokens_nettoyes_XML.txt"                                                    # Le fichier de tokens nettoyés
input_xml = "corpus_nettoye.xml"                                                                                                               # Le fichier XML d'entrée avec toutes les informations supplémentaires
output_xml = "corpus2.xml"                                  #"corpus_nettoye_definitif.xml"                                                    # Le fichier XML à générer avec les informations complètes

generer_xml(tokens_file, input_xml, output_xml)
