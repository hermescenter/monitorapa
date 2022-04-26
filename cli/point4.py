#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import configparser
import sys
import commons
import time


def usage():
    print("""
./cli/point4.py check/test_to_run.js out/202?-??-??/enti.tsv time_to_wait_in_seconds [start_index] [end_index]
""")
    sys.exit(-1)


def process(pa, message):

    print("Codice: " + pa[1] + ", Denominazione: " + pa[2] + ", nome: " + pa[12]
          + ", cognome: " + pa[13] + ", sito: " + pa[29].lower() + ", mail: " + pa[19], ", result: " + pa[35])

    final_msg = message.replace("$cod_amm", pa[1])
    final_msg = final_msg.replace("$des_amm", pa[2])
    final_msg = final_msg.replace("$nome_resp", pa[12])
    final_msg = final_msg.replace("$cogn_resp", pa[13])
    final_msg = final_msg.replace("$sito_istituzionale", pa[29].lower())

    return final_msg


def main(argv):
    if len(argv) > 5:
        usage()

    outDir = commons.computeOutDir(sys.argv)

    subject = "Diffida per violazione del GDPR per utilizzo Google Analytics su sito istituzionale"
    message = """Alla Att.ne del DPO (Responsabile Protezione Dati) dell'Ente.

Diffida per per l'illecito utilizzo di Google Analytics su
$cod_amm, in violazione del 
Regolamento generale sulla protezione dei dati personali 2016/679 (GDPR)

Spett.le Ente,
siamo un gruppo di hacker italiani, attiviste e attivisti, cittadine e
cittadini attenti alla privacy ed alla tutela dei diritti cibernetici
nel nostro Paese.

Abbiamo rilevato che il vostro Ente utilizza Google analytics (GA) 
nel suo sito $sito_istituzionale, nonostante sia oramai pacifico 
che questo strumento non sia conforme ai principi del GDPR in ordine
al trasferimento transfrontaliero di dati personali.
L'utilizzo di GA è infatti stato ritenuto illecito dall'EDPS, 
con riguardo al trattamento dei dati operato dal Parlamento europeo, 
dall'Autorità di controllo austriaca e da da ultimo da quella francese 
(si veda in sintesi https://noyb.eu/en/edps-sanctions-parliament-over-eu-us-data-transfers-google-and-stripe).

Riteniamo che il mantenimento, da parte dell'Ente, di un trattamento 
di dati personali così evidentemente illecito, che comporta un 
ingiustificato e massivo trasferimento trasfrontaliero di dati 
personali, riguardante tutti gli utenti del sito $sito_istituzionale, 
costituisca una grave violazione che debba immediatamente cessare.
Invitiamo pertanto a voler immediatamente provvedere alla rimozione 
di GA e di qualsiasi altro strumento di analytics o tracking che 
produca effetti analoghi.

La suddetta violazione, imputabile al Vs. Ente $des_amm, 
quale titolare del trattamento, in persona del legale rapp.te pro 
tempore $nome_resp $cogn_resp espone l'Ente stesso alle sanzioni
amministrative pecuniarie previste dall'art. 83 del GDPR.

La presente viene inviata in via informativa, proprio al fine di
consentire una rapida rimozione di Google Analytics, rimandando 
a quanto raccomandato dalla Agenzia per l'Italia Digitale Web Analytics Italia
https://www.agid.gov.it/it/design-servizi/web-analytics-italia

Il resoconto complessivo delle Pubbliche Amministrazioni in violazione,
con particolare riguardo a quelle che non avranno provveduto alla
tempestiva rimozione di GA, verrà pubblicato come report e inviato
come segnalazione al Garante per la Protezione dei Dati e
al Difensore Civico Digitale.

"""

    configParser = configparser.RawConfigParser()
    configParser.read('./cli/point4.cfg')
    config = dict(configParser.items('server-settings'))

    send_for_real = str(config['send_for_real'])

    smtp_server = str(config['smtp_server'])
    port = int(config['port'])
    sender_email = str(config['sender_email'])
    password = str(config['password'])
    receiver_email = str(config['debug_receiver_email'])

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)

        try:
            time_to_wait = int(argv[3])
        except:
            time_to_wait = 0
        try:
            start_index = int(argv[4])
        except:
            start_index = 0
        try:
            end_index = int(argv[5])
        except:
            end_index = -1

        count = 0
        with open(outDir + '/../point3/enti.tsv', 'r') as f:
            for line in f:
                if count > 0 and count >= start_index:
                    if end_index != -1 and count > end_index:
                        break
                    else:
                        fields = line.split('\t')

                        if (int(fields[35]) == 1):
                            msg = process(fields, message)

                            if send_for_real.lower() == "true":
                                # Rimpiazzare receiver_email con fields[19] quando si vuole mandare realmente le mail
                                final_msg=MIMEMultipart()
                                final_msg['From']=sender_email
                                final_msg['To']=receiver_email
                                final_msg['Subject']=subject
                                final_msg.attach(MIMEText(msg, 'plain'))
                                text=final_msg.as_string()

                                print(fields[19])
                                print(receiver_email)
                                server.sendmail(
                                    sender_email, receiver_email, text)
                   
                                time.sleep(time_to_wait)
                                

                count += 1


if __name__ == "__main__":
    main(sys.argv)
