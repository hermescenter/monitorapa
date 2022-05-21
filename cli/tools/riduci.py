'''
Questo script prende un enti.tsv prodotto da point3 e lo riduce alle righe dove è risultato presente GA.
'''

with open("enti.tsv", "r") as inf, open ("out_enti.tsv", "w") as outf:
    final_str = next(inf)
    for line in inf:
        line_args = line.split("\t")
        if line_args[35] == "1":
            final_str += line
        
    outf.write(final_str)