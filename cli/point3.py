#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

from fileinput import filename
import time
import sys
import os.path
from venv import create
import commons
import json


def usage():
    print("""
./cli/point3.py check/test_to_run.js out/202?-??-??/enti.tsv [format]

Will create out/YYYY-MM-DD/google_analytics/point3/enti.[format] (default format is TSV)

Format options: tsv, json
""")
    sys.exit(-1)


def getDate(fname):
    return time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(fname)))


def getTime(fname):
    return time.strftime("%H:%m:%S", time.gmtime(os.path.getctime(fname)))


def getFields(lineNum, outDir):
    fname = outDir + "/../point2/%s.OK.txt" % lineNum
    try:
        with open(fname, 'r') as f:
            content = f.read()
        if len(content) > 0:
            if " " in content or "d" in content or "x" in content or "X" in content:
                # website was WAY too slow or GA is somehow misconfigured
                return (0, '', getDate(fname), getTime(fname))
            return (1, content, getDate(fname), getTime(fname))
        else:
            return (0, '', getDate(fname), getTime(fname))
    except:
        fname = outDir + "/../point2/%s.ERR.txt" % lineNum
        if os.path.exists(fname):
            return (0, '', getDate(fname), getTime(fname))
        return (0, '', '', '')


def process_tsv(inf, outf, outDir):
     count = 0
     for line in inf:
            outf.write(line[:-1])
            if count == 0:
                outf.write(
                    "\tweb_test_result\tweb_test_metadata\tweb_test_date\tweb_test_time\n")
            else:
                outf.write("\t%s\t%s\t%s\t%s\n" % getFields(count, outDir))
            count += 1

def process_sql(inf, outf, outDir):
    count = 0
    for line in inf:
        line_values = line.split('\t')

        if count == 0:
            create_table_str = "CRATE TABLE IF NOT EXISTS point3 ( "
            create_table_str += "Codice_IPA varchar(7) PRIMARY KEY not null, " #Codice identificativo
            create_table_str += "_id int not null AUTO_INCREMENT unique, " #numeri incrementali
            create_table_str += "Denominazione_ente varchar(255) not null, " #Stringa
            create_table_str += "Codice_fiscale_ente int not null, "  #11 numeri
            create_table_str += "Tipologia varchar(255) not null," #Stringa
            create_table_str += "Codice_Categoria varchar(3) not null, " #Stringa tipo "L33"
            create_table_str += "Codice_natura varchar(4)," #4 numeri, può essere nullo
            create_table_str += "Codice_ateco varchar(8)," #3 numeri a 2 cifre separati da un punto tipo "11.22.33", può essere nullo
            create_table_str += "Ente_in_liquidazione varchar(1)," #1 carattere (S/N), può essere nullo
            create_table_str += "Codice_MIUR varchar(10)," #Stringa di 10 caratteri come: ALIC837005, può essere nullo
            create_table_str += "Codice_ISTAT varchar(8)," #8 numeri, può essere nullo
            create_table_str += "Acronimo varchar(255)," #Stringa, può essere nullo
            create_table_str += "Nome_responsabile varchar(255)," #Stringa, può essere nullo
            create_table_str += "Cognome_responsabile varchar(255)," #Stringa, può essere nullo
            create_table_str += "Titolo_responsabile varchar(255)," #Stringa, può essere nullo
            create_table_str += "Codice_comune_ISTAT varchar(6) not null," #6 numeri
            create_table_str += "Codice_catastale_comune varchar(4) not null," #Stringa di 4 caratteri
            create_table_str += "CAP varchar(5) not null," #5 numeri
            create_table_str += "Indirizzo varchar(255) not null," #Stringa
            create_table_str += "Mail1 varchar(255) not null," #Stringa
            create_table_str += "Tipo_Mail1 varchar(255) not null," #Stringa
            create_table_str += "Mail2 varchar(255)," #Stringa, può essere nullo
            create_table_str += "Tipo_Mail2 varchar(255)," #Stringa, può essere nullo
            create_table_str += "Mail3 varchar(255)," #Stringa, può essere nullo
            create_table_str += "Tipo_Mail3 varchar(255)," #Stringa, può essere nullo
            create_table_str += "Mail4 varchar(255)," #Stringa, può essere nullo
            create_table_str += "Tipo_Mail4 varchar(255)," #Stringa, può essere nullo
            create_table_str += "Mail5 varchar(255)," #Stringa, può essere nullo
            create_table_str += "Tipo_Mail5 varchar(255)," #Stringa, può essere nullo
            create_table_str += "Sito_istituzionale varchar(255)," #Stringa, può essere nullo
            create_table_str += "Url_facebook varchar(255)," #Stringa, può essere nullo
            create_table_str += "Url_linkedin varchar(255)," #Stringa, può essere nullo
            create_table_str += "Url_twitter varchar(255)," #Stringa, può essere nullo
            create_table_str += "Url_youtube varchar(255)," #Stringa, può essere nullo
            create_table_str += "Data_aggiornamento varchar(10) not null," #Data nel formato 2018-06-05
            create_table_str += "web_test_result int not null," #1 numero, 0 o 1
            create_table_str += "web_test_metadata varchar(13)," #String, tipo UA-42647587-1
            create_table_str += "web_test_date varchar(10) not null," #Data nel formato 2022-03-23
            create_table_str += "web_test_time varchar(8) not null" #Ora nel formato 12:13:14
            create_table_str += ");"

            outf.write(create_table_str + "\n")

        else:
            insert_str = "INSERT INTO point3 VALUES ("

            for i in range(len(line_values)):
                if i != 0:
                    insert_str += "`" + line_values[i] + "`,"
            
            fields = getFields(count, outDir)
            for field in fields:
                if isinstance(field, str):
                    insert_str += "'" + field + "',"
                elif isinstance(field, int):
                    insert_str += str(field) + ","

            insert_str = insert_str[:-1]
            insert_str += ");\n"

            outf.write(insert_str)
        count += 1

def process_json(inf, outf, outDir):
    result = {}
    count = 0
    fields_names = []
    for line in inf:
        fields = line.split('\t')
        if count == 0 :
            fields_names = fields
        else:    
            result[fields[1]] = {}
            index = 0
            for field_name in fields_names:
                result[fields[1]][field_name] = fields[index]
                index += 1
            
            extra_fields = getFields(count, outDir)
            
            result[fields[1]]["web_test_result"] = extra_fields[0]
            result[fields[1]]["web_test_metadata"] = extra_fields[1]
            result[fields[1]]["web_test_date"] = extra_fields[2]
            result[fields[1]]["web_test_time"] = extra_fields[3]
            
        count += 1
    
    outf.write(json.dumps(result, indent=4))


def main(argv):
    if len(argv) > 4:
        usage()

    outDir = commons.computeOutDir(sys.argv)
    print(outDir)

    format = "tsv"

    if len(argv) > 3 and argv[3]:
        if argv[3] != "json" and argv[3] != "tsv" and argv[3] != "sql":
            usage()
        format = argv[3]

   
    with open(argv[2], 'r', encoding='utf-8-sig') as inf, open(outDir + '/enti.'+format, 'w') as outf:
        globals()['process_'+format](inf, outf, outDir)


if __name__ == "__main__":
    main(sys.argv)
