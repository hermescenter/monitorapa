import csv
import requests
import datetime
import time

def check_url(url, timeout):
    try:
        request = requests.get(url, timeout=timeout, allow_redirects=False)
        # request.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        return 0, "Http Error:" + str(errh)
    except requests.exceptions.ConnectionError as errc:
        return 0, "Error Connecting:" + str(errc)
    except requests.exceptions.Timeout as errt:
        return 0, "Timeout Error:" + str(errt)
    except requests.exceptions.RequestException as err:
        return 0, "OOps: Something Else" + str(err)
    except:
        return 0, "Error"
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

load_tsv()
first_line_header_tsv = True
filename_output = "../out/output.tsv"
# Create file output
f = open(filename_output, "w", encoding='UTF8', newline='').close()

reader = csv.reader( open("enti.tsv", "r", encoding='UTF8'), delimiter="\t" )
for row in reader:
    
    # Open file to append data
    f = open(filename_output, "a", encoding='UTF8', newline='')
    w = csv.writer(f, delimiter="\t")

    des = row[2]
    tip = row[4]
    url = row[29].lower().strip()
    check_date = datetime.datetime.now()
    
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

    check_http, code_http = check_url(url_http, 4)
    check_https, code_https = check_url(url_https, 4)
    
    print("--- --- --- --- --- --- ---")
    print(des[0:60], "\t" , url)
    print(url_http, " : ", check_http, code_http)
    print(url_https, " : ", check_https, code_https)

    row_tsv = [des, tip, url, check_date, check_http, check_https]
    
    w.writerow(row_tsv)
    f.close()