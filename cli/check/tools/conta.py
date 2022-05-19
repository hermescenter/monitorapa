'''
Questo file prende in input un enti.tsv ordinato per Codice_Categoria. 
Se siete su LibreOffice è facilissimo: aprite il tsv (mi raccomando impostate la separazione sul tab),
selezionate una cella della colonna Codice_Categoria, in alto fate Dati > Ordina, lasciate tutto a predefinito e date Ok.
Fatto li abbiamo ordinati per Codice_Categoria.
'''


final_dict = {}

with open("enti.tsv", 'r') as inf:
    next(inf)


    curr_field = ""
    current_count = 0
    for line in inf:
        line_values = line.split('\t')

        if curr_field == "":
            curr_field = line_values[5]

        if curr_field != line_values[5]:
            final_dict[curr_field] = current_count

            curr_field = line_values[5]
            current_count = 0

        if line_values[35] == "1":
            current_count += 1


with open("result.tsv", 'w') as inf:
    first_line =""
    second_line = ""
    for key  in final_dict:
        first_line += key +"\t"
        second_line += str(final_dict[key]) + "\t"
    
    inf.write(first_line + "\n" + second_line)