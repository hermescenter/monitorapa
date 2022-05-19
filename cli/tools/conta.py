'''
Questo file prende in input un enti.tsv ed un categorie.tsv (https://indicepa.gov.it/ipa-dati/dataset/categorie-enti) ordinato per Codice_Categoria. 
Se siete su LibreOffice è facilissimo: aprite il tsv (mi raccomando impostate la separazione sul tab),
selezionate una cella della colonna Codice_Categoria, in alto fate Dati > Ordina, lasciate tutto a predefinito e date Ok.
Fatto li abbiamo ordinati per Codice_Categoria.
'''


from typing import final


final_dict = {}

with open("enti.tsv", 'r') as inf, open("categorie.tsv", 'r') as inf_categorie:
    next(inf)
    next(inf_categorie)

    curr_field = ""
    curr_name = ""
    current_count = 0
    total_count = 0
    for line in inf:
        line_values = line.split('\t')

        if curr_field == "":
            curr_field = line_values[5]
            curr_name = next(inf_categorie).split('\t')[2]

        if curr_field != line_values[5]:
            final_dict[curr_field] = {"count": current_count, "name": curr_name, "total": total_count}

            curr_name = next(inf_categorie).split('\t')[2]

            curr_field = line_values[5]
            current_count = 0
            total_count = 0
            

        if line_values[35] == "1":
            current_count += 1

        total_count += 1


with open("result.tsv", 'w') as inf:
    final_str = ""

    for key  in final_dict:
        final_str += key +"\t"
        final_str += str(final_dict[key]["count"]) + "\t"
        final_str += str(final_dict[key]["total"]) + "\t"
        final_str += str(final_dict[key]["count"] * 100 / final_dict[key]["total"]) + "%\t"
        final_str += str(final_dict[key]["name"]) + "\n"
    
    inf.write(final_str)