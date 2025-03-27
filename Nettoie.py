def nettoyer_fichier_tokens(fichier_entree, fichier_sortie):
    with open(fichier_entree, 'r', encoding='utf-8') as f_in, open(fichier_sortie, 'w', encoding='utf-8') as f_out:
        for ligne in f_in:
            token, bulletin_num = ligne.strip().split('\t')
            if token != "''":
                f_out.write(f"{token}\t{bulletin_num}\n")

fichier_entree = "X6 - TokensFiltres.txt"
fichier_sortie = "X7 - Tokens_nettoyes_XML.txt"  

nettoyer_fichier_tokens(fichier_entree, fichier_sortie)
