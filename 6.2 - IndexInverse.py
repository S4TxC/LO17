import xml.etree.ElementTree as ET

def generer_index_inverse(input_xml, output_dir):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    index_titre = {}
    index_rubrique = {}
    index_date = {}
    index_lemmes = {}
    index_urls = {}
    index_contacts = {}

    for bulletin in root.findall("bulletin"):
        bulletin_num = bulletin.find("fichier").text
        
        titre = bulletin.find("titre").text if bulletin.find("titre") is not None else ""
        rubrique = bulletin.find("rubrique").text if bulletin.find("rubrique") is not None else ""
        date = bulletin.find("date").text if bulletin.find("date") is not None else ""
        contact = bulletin.find("contact").text if bulletin.find("contact") is not None else ""
        
        lemmes = bulletin.find("tokenisation").text if bulletin.find("tokenisation") is not None else ""
        if lemmes:
            lemmes = lemmes.split()

        if titre:
            if titre not in index_titre:
                index_titre[titre] = {}
            if bulletin_num not in index_titre[titre]:
                index_titre[titre][bulletin_num] = 0
            index_titre[titre][bulletin_num] += 1
        
        if rubrique:
            if rubrique not in index_rubrique:
                index_rubrique[rubrique] = {}
            if bulletin_num not in index_rubrique[rubrique]:
                index_rubrique[rubrique][bulletin_num] = 0
            index_rubrique[rubrique][bulletin_num] += 1
        
        if date:
            if date not in index_date:
                index_date[date] = {}
            if bulletin_num not in index_date[date]:
                index_date[date][bulletin_num] = 0
            index_date[date][bulletin_num] += 1

        if lemmes:
            for lemme in lemmes:
                if lemme not in index_lemmes:
                    index_lemmes[lemme] = {}
                if bulletin_num not in index_lemmes[lemme]:
                    index_lemmes[lemme][bulletin_num] = 0
                index_lemmes[lemme][bulletin_num] += 1

        if contact:
            if contact not in index_contacts:
                index_contacts[contact] = {}
            if bulletin_num not in index_contacts[contact]:
                index_contacts[contact][bulletin_num] = 0
            index_contacts[contact][bulletin_num] += 1

        images = bulletin.find("images")
        if images is not None:
            for image in images.findall("image"):
                url = image.find("urlImage").text if image.find("urlImage") is not None else ""

                if url:
                    for mot in url.split():
                        if mot not in index_urls:
                            index_urls[mot] = {}
                        if bulletin_num not in index_urls[mot]:
                            index_urls[mot][bulletin_num] = 0
                        index_urls[mot][bulletin_num] += 1

    def fichier_index_inverse(index, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for term, doc_freqs in index.items():
                doc_list = [f"{doc_id}:{freq}" for doc_id, freq in doc_freqs.items()]
                total_occurrences = sum(doc_freqs.values())
                f.write(f"{term}\t" + ", ".join(doc_list) + f"\tTotal: {total_occurrences}\n")

    fichier_index_inverse(index_titre, f"{output_dir}/index_titre.txt")
    fichier_index_inverse(index_rubrique, f"{output_dir}/index_rubrique.txt")
    fichier_index_inverse(index_date, f"{output_dir}/index_date.txt")
    fichier_index_inverse(index_lemmes, f"{output_dir}/index_lemmes.txt")
    fichier_index_inverse(index_urls, f"{output_dir}/index_images_urls.txt")
    fichier_index_inverse(index_contacts, f"{output_dir}/index_contacts.txt")

input_xml = "corpus3.xml"
output_dir = "index_inverses"

generer_index_inverse(input_xml, output_dir)
