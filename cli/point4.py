#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import smtplib
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

    message = """\
Subject: Diffida per violazione della normativa in materia privacy, Regolamento UE 679/2016 e norme applicative, per utilizzo Google Analytics su $cod_amm

Alla Att.ne del DPO (Responsabile Protezione Dati) dell'Ente. Oggetto: Diffida per violazione del GDPR per utilizzo Google Analytics su sito istituzionale La presente comunicazione valga come formale diffida, per segnalare violazione del Regolamento Ue 679/2016 in materia privacy, posta in essere dal vs. Ente $des_amm con responsabile Dott. $nome_resp $cogn_resp derivante dall'utilizzo presso il sito $sito_istituzionale del fornitore Google, secondo quanto confermato dalla decisione dell'EDPS nell'arrivare a sanzionare il Parlamento Europeo per l'uso dello strumento Google Analytics come indicato in seguito https://noyb.eu/en/edps-sanctions-parliament-over-eu-us-data-transfers-google-and-stripe . La presente viene inviata in via informativa per consentire una rapida rimozione di Google Analytics, rimandando raccomandato dalla Agenzia per l'Italia Digitale Web Analytics Italia https://www.agid.gov.it/it/design-servizi/web-analytics-italia . Il rendiconto delle Pubbliche Amministrazioni in violazione viene pubblicato come report e inviato come segnalazione al Garante per la Protezione dei Dati e al Difensore Civico Digitale."""

    configParser = configparser.RawConfigParser()
    configParser.read('./cli/point4.cfg')
    config = dict(configParser.items('server-settings'))

    send_for_real = str(config['send_for_real'])

    smtp_server = str(config['smtp_server'])
    port = int(config['port'])
    sender_email = str(config['sender_email'])
    password = str(config['password'])
    receiver_email = str(config['debug_receiver_email'])

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
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
                                server.sendmail(
                                    sender_email, receiver_email, msg)
                                time.sleep(time_to_wait)

                count += 1


if __name__ == "__main__":
    main(sys.argv)
