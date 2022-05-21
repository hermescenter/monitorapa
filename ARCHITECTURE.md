# Architettura dell'osservatorio automatico distribuito di Monitora PA

```
This file is part of MonitoraPA

Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>

MonitoraPA is a hack. You can use it according to the terms and
conditions of the Hacking License https://monitora-pa.it/LICENSE.txt
```

## Obiettivo

Il sistema di monitoraggio deve essere semplice da eseguire ed estendere
per chiunque conosca un minimo Python, nonché banale da manutenere

Non necessita di essere scalabile, enterprise, cool etc...

## Tipi di componenti

- sorgenti dato
- verifiche
- segnalazioni 
- reportistica
- tools

la comunicazione fra i componenti avviene attraverso file tsv dal
formato convenzionale in modo da limitare a python il set di conoscenze
necessarie per comprendere e manutenere il codice limitare ad un editor
di testo il necessario per ispezionarli


## Sorgenti di dato

Il sistema deve poter applicare le verifiche a diversi tipi di dataset

I comandi relativi alle diverse sorgenti dato stanno dentro sottocartelle
di ./cli/data/ ad esempio

```
./cli/data
  enti/
    download.py
    normalize.py
  scuola/
    normalize.py
  partiti/
    download.py
    normalize.py
  ...
```  
`./cli/data/enti/download.py`

scarica il dataset enti nella cartella ./out/enti/YYYY-MM-YY/enti.tsv

`./cli/data/enti/normalize.py ./out/enti/YYYY-MM-YY/enti.tsv`

crea il file ./out/enti/YYYY-MM-YY/dataset.tsv che contiene i seguenti campi
- ID
- Type
- Address

ID è l'identificativo univoco all'interno della sorgente dati 
(il numero di righa se non esiste alcun indentificativo univoco)

Type può essere uno dei seguenti valori:
- Web
- Email

Address è l'indirizzo di un automatismo dell'ente da testare.

Prima di salvare il file lo script verifica che non ci siano righe duplicate

In sostanza, dataset.tsv contiene l'elenco degli automatismi da testare
associati a ciascun ente.


## Verifiche

Dopo l'eventuale scaricamento e la normalizzazione del dataset sarà
possibile avviare le verifiche, anche in parallelo.

Tutti gli script di verifica prendono come primo argomento il path del
file dataset.tsv

Gli script leggono le righe del file dataset e, se il Type è di loro
competenza, effettuano i propri controlli.

Non possono avere parametri opzionali.

Se il file di output esiste già, individuano l'ultima riga nell'output
ed ignorano tutte le righe che la precedono nel dataset.

Scrivono un file tsv che contiene il seguente tracciato
- ID
- Type
- Address
- Time
- Completed
- Issues

Time contiene data ed ora di completamento del test

Completed: 0 il test non è stato completato 1 il test è stato completato

Issues: la semantica dipende dal valore del campo Completed

- `Completed = 1` => metadati perché il test ha riscontrato 
  un problema nell'ente identificato da ID
- `Completed = 0` => l'errore che ha impedito il completamento del test

I dati salvati nel campo Issues non possono contenere tab o newline, 
che andranno sostituiti con uno spazio prima di aggiungerli al file

``` 
./cli/check/
  http.py <- script precedentemente proposto da Emilie
  selenium.py <- attuale point2.py
  selenium/   <- cartella che contiene i test da effettuare via browser
    google_analytics.js <- test per la presenza di Google Analytics
    google_font.js      <- test per la presenza di Google Fonts
    google_maps.js      <- test per la presenza di Google Maps
    google_youtube.js   <- test per la presenza di video YouTube
    facebook_pixel.js   <- test per la presenza di Facebook Pixel
    ...
  smtp.py <- script di verifica del record mx delle mail istituzionali per
             - individuare chi usa GMail o Outlook 365 con una mail non
               chiaramente riferibili a questi fornitori
               (host -t mx dominio)
             - verificare che il server SMTP accetti solo connessioni
               cifrate etc...
  ...
``` 

Ogni script di verifca scrive nella cartella del dataset iniziale
un file tsv con il suo stesso nome, ad esempio

`./cli/check/http.py ./out/enti/YYYY-MM-DD/dataset.tsv`
scriverà il proprio output in ./out/enti/YYYY-MM-DD/check/http.tsv

`./cli/check/smpt.py ./out/enti/YYYY-MM-DD/dataset.tsv`
scriverà il proprio output in ./out/enti/YYYY-MM-DD/check/smpt.tsv

`./cli/check/browse,py ./out/enti/YYYY-MM-DD/dataset.tsv google_analytics`
scriverà il proprio output in ./out/enti/YYYY-MM-DD/check/google_analytics.tsv

Ogni check può utilizzare una cartella con il proprio nome, dentro
check/ per eventuali dati temporanei


# Segnalazioni

Lo script di invio della segnalazione legge tutti i file prodotti
dal check e per ogni riga con Completed a 1 e Issue valorizzata
puoi inviare una PEC all'ente, ricercando l'indirizzo all'interno del
file enti.tsv

L'invio delle segnalazioni avviene da un server diverso rispetto
a quello in cui viene eseguito il monitoraggio, in modo da rendere
la vita più difficile ad un eventuale attaccante.

# Report

ad ogni script dentro check corrisponde uno script in ./cli/report/
che produce un report dedicato a partire dai dati racolti durante le
verifiche

Ad esempio
`./cli/report/http.py` <- produce il report dell'evoluzione di 
questa statistica nel tempo

`./cli/check/http.py ./out/enti/YYYY-MM-DD/dataset.tsv`
scriverà il proprio output in ./out/enti/YYYY-MM-DD/report/http.png o ./out/enti/YYYY-MM-DD/report/http.html

# Tool

Strumenti di sviluppo non eseguiti automaticamente dall'osservatorio.

___


# Bozza MD nuova struttura

```
monitorapa
│
│   README.md
│   PROGRESS.md
│   LICENCE.txt
│   AUTHORS.md
│   ARCHITECTURE.md
│   MANUAL.md
|   SPECIFICATION.md (specifica del vecchio sistema, sostituito da ARCHITECTURE.md)
│   .gitignore
│
└───docker
│   │   start.sh
│   │   docker-compose.yml
│   │   Dockerfile
│   │   Dockerfile-base
│
└───cli
│   │   runAll.py <- Esegue TUTTO tranne le PEC
│   │
│   └───data
│   │   │ 
│   │   └───enti
│   │   │   │   download.py <- scarica out/enti/YYYY-MM-DD/enti.tsv
│   │   │   │   normalize.py <- produce out/enti/YYYY-MM-DD/dataset.tsv
│   │   │
│   │   └───scuola
│   │   │   │   normalize.py <- produce out/scuola/YYYY-MM-DD/dataset.tsv
│   │   │
│   │   └───partiti
│   │   │   │   download.py <- scarica out/partiti/YYYY-MM-DD/enti.tsv
│   │   │   │   normalize.py <- produce out/partiti/YYYY-MM-DD/dataset.tsv
│   │   
│   └───check
│   │   │   http.py <- produce out/*/YYYY-MM-DD/check/http.tsv
│   │   │   smtp.py <- produce out/*/YYYY-MM-DD/check/smtp.tsv
│   │   │   selenium.py <- produce out/*/YYYY-MM-DD/check/browse/*/*.tsv
│   │   │   selenium/
│   │   │   │   google_analytics.js <- test per la presenza di Google Analytics
│   │   │   │   google_font.js      <- test per la presenza di Google Fonts
│   │   │   │   google_maps.js      <- test per la presenza di Google Maps
│   │   │   │   google_youtube.js   <- test per la presenza di video YouTube
│   │   │   │   facebook_pixel.js   <- test per la presenza di Facebook Pixel
│   │   
│   └───report
│   │   │   http.py <- produce out/*/YYYY-MM-DD/report/http.html/png
│
└───out
│   │
│   └───enti
│   │   │
│   │   └───YYYY-MM-DD
│   │   │   │   enti.tsv
│   │   │   │   dataset.tsv
│   │   │   │
│   │   │   └───check
│   │   │   │   │   http.tsv
│   │   │   │   │   smtp.tsv
│   │   │   │   │   browse/
│   │   │   │   │   │   google_analytics.tsv
│   │   │   │
│   │   │   └───report
│   │   │   │   │   http.png
│   │
│   └───scuola
│   │   │
│   │   └───YYYY-MM-DD
│   │   │   │   enti.tsv
│   │   │   │   dataset.tsv
│   │   │   │
│   │   │   └───check
│   │   │   │   │   http.tsv
│   │   │   │   │   smtp.tsv
│   │   │   │   │   google_analytics.tsv
│   │   │   │
│   │   │   └───report
│   │   │   │   │   http.png
```

