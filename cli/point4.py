#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
import ssl
import configparser
import sys
import datetime
import commons
import os
import time
from email.message import EmailMessage


def usage():
    print("""
./cli/point4.py check/test_to_run.js out/202?-??-??/enti.tsv time_to_wait_in_seconds
""")
    sys.exit(-1)


def process(pa, message):

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

    subject = """Segnalazione di illecito utilizzo di Google Analytics su $cod_amm, ed invito a risolvere la violazione del Regolamento generale sulla protezione dei dati personali 2016/679 (GDPR) all'interno del sito web $sito_istituzionale"""
    message = """All'att.ne di $cod_amm, in qualità di soggetto titolare 
del trattamento ai sensi dell'art. 4 par. 1 n. 7) GDPR.

Il sottoscritto Fabio Pietrosanti scrive in proprio nonché a nome e per 
conto delle associazioni firmatarie in calce e della comunità di hacker,
attiviste e attivisti, cittadine e cittadini italiani attenti alla
riservatezza, alla libertà ed ai diritti cibernetici che ha realizzato
Monitora PA https://monitora-pa.it , eleggendo domicilio digitale presso
l'indirizzo di posta elettronica certificata monitorapa@peceasy.it,
nonché domicilio fisico presso _inserire domicio fisico_ . 

Facciamo seguito alla PEC inviata in data $primo_invio per rilevare che
il vostro Ente utilizza ancora Google Analytics (GA) nel suo sito
$sito_istituzionale, nonostante questo strumento non sia attualmente
conforme, in assenza di misure tecniche supplementari efficaci,
alle disposizioni del GDPR in ordine al trasferimento transfrontaliero
di dati personali e alle "Linee guida cookie e altri strumenti di
tracciamento" approvate dall'Autorità garante per la protezione dei
dati personali il 10 giugno 2021.

Come ben noto, anche a seguito della sentenza Schrems II della Corte di
Giustizia dell'Unione Europea, l'utilizzo di GA è stato ritenuto illecito
dall'EDPS, dall'Autorità di controllo austriaca e da ultimo da quella
francese.

Riteniamo che il mantenimento, da parte dell'Ente, di un trattamento di
dati personali non conforme al disposto normativo, in ragione del
trasferimento trasfrontaliero di dati personali in assenza di una
condizione legittimante ai sensi degli artt. 44 e ss. GDPR, esponga 
a rischi ingiustificati tutti i visitatori del sito $sito_istituzionale.

Pertanto invitiamo nuovamente l'Ente in indirizzo a voler provvedere 
alla rimozione di GA e di qualsiasi altro strumento di analytics o
tracking che produca effetti analoghi, entro il termine di 15 giorni
dalla ricezione della presente oppure, in alternativa, adottare misure
tecniche supplementari efficaci a protezione dei dati personali dei
visitatori, in modo tale che nessun dato (o insieme di dati) che possa
permettere a Google di identificare con una probabilità utile un
qualsiasi cittadino italiano o europeo, possa raggiungere server
controllati da tale azienda.

In difetto di ottemperanza da parte Vostra agli obblighi di legge in
materia di trattamento dei dati personali nei termini sopra indicati,
inoltreremo segnalazione al Garante per la protezione dei dati personali
ai sensi e per gli effetti dell'art. 144 del Codice in materia di
protezione dei dati personali (DECRETO LEGISLATIVO 30 giugno 2003, n.196
e successive modifiche ed integrqazioni) per la valutazione della
Vostra condotta anche ai fini dell'emanazione dei provvedimenti
di cui all'art. 58 del GDPR.

Con osservanza.

Distinti saluti


Fabio Pietrosanti
Co-fondatore di Monitora PA
https://monitora-pa.it

con il sostegno di

- Copernicani
  https://copernicani.it/

- Hermes Center
  https://www.hermescenter.org/

- LinuxTrent
  https://www.linuxtrent.it/

- Open Genova
  https://associazione.opengenova.org/

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

    a = datetime.datetime(2022,5,11,17,2,20)


    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)

        try:
            time_to_wait = int(argv[3])
        except:
            time_to_wait = 0
        
        count = 0
        out_count = 1

        if not os.path.exists(outDir + '/../point4/log.tsv'):
            open(outDir + '/../point4/log.tsv', 'w').close()

        with open(outDir + '/../point3/enti.tsv', 'r') as f, open(outDir + '/../point4/log.tsv', 'r+') as logf:
            length = len(logf.readlines())
            if length == 0:   
                logf.write("Codice_IPA\tMail1\tSito_istituzionale\tData\n")
            else:
                out_count = length + 3


            for line in f:
                if count >= out_count:
                  
                    fields = line.split('\t')

                    if (int(fields[35]) == 1):
                        subject = process(fields, subject)
                        msg = process(fields, message)
                        
                        print("Codice: " + fields[1] + ", Denominazione: " + fields[2] + ", nome: " + fields[12]
          + ", cognome: " + fields[13] + ", sito: " + fields[29].lower() + ", mail: " + fields[19], ", result: " + fields[35])

                        if send_for_real.lower() == "true":
                            # Rimpiazzare receiver_email con fields[19] quando si vuole mandare realmente le mail
                            final_msg = EmailMessage()
                            final_msg['From']=sender_email

                            final_msg['To']=receiver_email #per provare in debug: receiver_email altrimenti fields[19]
                            final_msg['Cc']=sender_email #Per vedere le mail che mandiamo, Bcc non pare essere accettato.

                            final_msg['Subject']=subject
                            final_msg.set_content(msg)

                            print(fields[19])
                            print(receiver_email)
                            
                            b = a + datetime.timedelta(seconds=count*10)

                            #server.send_message(final_msg)
                            logf.write("%s\t%s\t%s\t%s\n" % (fields[1], fields[19], fields[29], str(datetime.datetime.now())))
                        
                            time.sleep(time_to_wait)

                count += 1


if __name__ == "__main__":
    main(sys.argv)
