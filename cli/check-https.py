#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
# Copyright (C) 2022 Emilie Rollandin <emilie@rollandin.it>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import csv
import requests
import datetime
import time
import sys

def check_url(url, timeout):
    try:
        request = requests.get(url, timeout=timeout, allow_redirects=False)
    except requests.exceptions.HTTPError:
        return 0, "Http Error"
    except requests.exceptions.ConnectionError:
        return 0, "Error Connecting"
    except requests.exceptions.Timeout:
        return 0, "Timeout Error"
    except requests.exceptions.RequestException:
        return 0, "Ops: Something Else"
    else:
        return 1, request

def make_complete_url(url):
    if('http://' in url):
        url_http = url
        url_https = url.replace("http://", "https://")
    elif('https://' in url):
        url_http = url.replace("https://", "http://")
        url_https = url
    else:
        url_http = 'http://' + url
        url_https = 'https://' + url

    return url_http, url_https


def load_tsv():
    # Load "enti.tsv" - point1.py
    outDir = "."
    url = 'https://indicepa.gov.it/ipa-dati/datastore/dump/d09adf99-dc10-4349-8c53-27b1e5aa97b6?bom=True&format=tsv'
    r = requests.get(url, allow_redirects=True)
    result = r.content.replace(
        b'HTTPS:SISTEMAAMBIENTELUCCA.IT', b'HTTPS://SISTEMAAMBIENTELUCCA.IT')
    open("%s/enti.tsv" % outDir, 'wb').write(result)
    print("%s/enti.tsv" % outDir)

# main
skip_rows = 0
skip = False
first_line_header_tsv = False
filename_output = "../out/output_check_https.tsv"

# possibilità di skippare alla riga n.
if len(sys.argv) == 2:
    skip_rows = int(sys.argv[1])

if(skip_rows != 0):
    skip = True

load_tsv()

# Create file output
if not skip:
    f = open(filename_output, "w", encoding='UTF8', newline='').close()
    first_line_header_tsv = True

reader = csv.reader( open("enti.tsv", "r", encoding='UTF8'), delimiter="\t" )
for row in reader:

    if skip:
        try:
            for i in range(skip_rows):
                next(reader)
        except StopIteration:
            break
        except Exception as e:
            raise e
        finally:
            skip = False
            continue
    
    # Open file to append data
    f = open(filename_output, "a", encoding='UTF8', newline='')
    w = csv.writer(f, delimiter="\t")

    des = row[2]
    tip = row[4]
    url = row[29].lower().strip()
    check_date = datetime.datetime.now()
    
    if not skip:
        if(first_line_header_tsv):
            first_line_header_tsv = False
            row_tsv = [des, tip, url, "check_date", "check_http", "check_https"]
            w.writerow(row_tsv)
            continue

    if (url in (None, '')) or (len(url) < 4):
        row_tsv = [des, tip, url, check_date, 0, 0]
        continue

    # make complete url with http:// and https://
    url_http, url_https = make_complete_url(url)

    check_http = 0
    check_https = 0
    code_http = ""
    code_https = ""

    check_http, code_http = check_url(url_http, 4)
    check_https, code_https = check_url(url_https, 4)
    
    print("--- --- --- --- --- --- ---")
    print(des[0:60], "\t" , url)
    print(url_http, " : ", check_http, code_http)
    print(url_https, " : ", check_https, code_https)

    row_tsv = [des, tip, url, check_date, check_http, check_https]
    
    w.writerow(row_tsv)
    f.close()