import xml.etree.ElementTree as ET
from collections import defaultdict

def generer_index_inverse(input_xml, output_dir):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    index_titre = {}
    index_rubrique = {}
    index_date = {}
    index_lemmes = {}

    for bulletin in root.findall("bulletin"):
        bulletin_num = bulletin.find("fichier").text
        
        titre = bulletin.find("titre").text if bulletin.find("titre") is not None else ""
        rubrique = bulletin.find("rubrique").text if bulletin.find("rubrique") is not None else ""
        date = bulletin.find("date").text if bulletin.find("date") is not None else ""
        
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

    def write_index_to_file(index, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for term, doc_freqs in index.items():
                doc_list = [f"{doc_id}:{freq}" for doc_id, freq in doc_freqs.items()]
                total_occurrences = sum(doc_freqs.values())
                f.write(f"{term}\t" + ", ".join(doc_list) + f"\tTotal: {total_occurrences}\n")

    write_index_to_file(index_titre, f"{output_dir}/index_titre.txt")
    write_index_to_file(index_rubrique, f"{output_dir}/index_rubrique.txt")
    write_index_to_file(index_date, f"{output_dir}/index_date.txt")
    write_index_to_file(index_lemmes, f"{output_dir}/index_lemmes.txt")

input_xml = "corpus3.xml"
output_dir = "index_inverses"

generer_index_inverse(input_xml, output_dir)
