#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import smtplib, ssl
import configparser
import sys

def usage():
    print("""
./cli/point4.py [optional=start_index] [optional=end_index]
""")
    sys.exit(-1)

def process(pa, server, sender_email, receiver_email, message):

    final_msg = message.replace("$cod_amm", pa[0])
    final_msg = final_msg.replace("$des_amm", pa[1])
    final_msg = final_msg.replace("$nome_resp", pa[2])
    final_msg = final_msg.replace("$cogn_resp", pa[3])
    final_msg = final_msg.replace("$sito_istituzionale", pa[8])

    return final_msg

def main(argv):
    if len(argv) > 3:
        usage()

    message = """\
Subject: Diffida per violazione della normativa in materia privacy, Regolamento UE 679/2016 e norme applicative, per utilizzo Google Analytics su $cod_amm

Alla Att.ne del DPO (Responsabile Protezione Dati) dell'Ente. Oggetto: Diffida per violazione del GDPR per utilizzo Google Analytics su sito istituzionale La presente comunicazione valga come formale diffida, per segnalare violazione del Regolamento Ue 679/2016 in materia privacy, posta in essere dal vs. Ente $des_amm con responsabile Dott. $nome_resp $cogn_resp derivante dall'utilizzo presso il sito $sito_istituzionale del fornitore Google, secondo quanto confermato dalla decisione dell'EDPS nell'arrivare a sanzionare il Parlamento Europeo per l'uso dello strumento Google Analytics come indicato in seguito https://noyb.eu/en/edps-sanctions-parliament-over-eu-us-data-transfers-google-and-stripe . La presente viene inviata in via informativa per consentire una rapida rimozione di Google Analytics, rimandando raccomandato dalla Agenzia per l'Italia Digitale Web Analytics Italia https://www.agid.gov.it/it/design-servizi/web-analytics-italia . Il rendiconto delle Pubbliche Amministrazioni in violazione viene pubblicato come report e inviato come segnalazione al Garante per la Protezione dei Dati e al Difensore Civico Digitale."""

    configParser = configparser.RawConfigParser()
    configParser.read('./point4.cfg')
    config = dict(configParser.items('server-settings'))

    smtp_server=str(config['smtp_server'])
    port=int(config['port'])
    sender_email=str(config['sender_email'])
    password=str(config['password'])
    receiver_email=str(config['debug_receiver_email'])

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)

        try:
            start_index = int(argv[1])
        except:
            start_index = 0
        try:
            end_index = int(argv[2])
        except:
            end_index = 0

        count = 0
        with open('point3.amministrazioni.txt', 'r') as f:
            for line in f:
                if count > 0 and count >= start_index and count <= end_index:
                    fields = line.split('\t')
                    
                    msg = process(fields, server, sender_email, receiver_email, message)
                    server.sendmail(sender_email, receiver_email, msg)

                count += 1

if __name__ == "__main__":
    main(sys.argv)
