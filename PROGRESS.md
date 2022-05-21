# Progress

## 2022/01/31
### Naif
- First commit
- README.md with:
    - description
    - requirements
    - point1
    - point2
    - point3
    - point4
    - point5

## 2022/02/02
### Shamar
- Added Hacking license
- point1 (using [amministrazioni.txt](https://indicepa.gov.it/ipa-dati/dataset/502ff370-1b2c-4310-94c7-f39ceb7500e3/resource/3ed63523-ff9c-41f6-a6fe-980f3d9e501f/download/amministrazioni.txt) )
- point2 (using [amministrazioni.txt](https://indicepa.gov.it/ipa-dati/dataset/502ff370-1b2c-4310-94c7-f39ceb7500e3/resource/3ed63523-ff9c-41f6-a6fe-980f3d9e501f/download/amministrazioni.txt) )
- MANUAL with instructions on how to install the requirements for the project on Debian
- google_analytics check script

## 2022/02/06
### \_Zaizen\_
- Matrix link updated
- python venv setup instructions
- point4
- point2 beginning index parameter

### Shamar
- google_analytics check script updated
- point3
- Instructions to run scripts

## 2022/02/07
### \_Zaizen\_
- point2 skip empty links

### Shamar
- point2 url validation
- google_analytics check script updated

## 2022/02/09
### Shamar
- Switched the whole project to [enti.tsv](https://indicepa.gov.it/ipa-dati/datastore/dump/d09adf99-dc10-4349-8c53-27b1e5aa97b6?bom=True&format=tsv) insead of [amministrazioni.txt](https://indicepa.gov.it/ipa-dati/dataset/502ff370-1b2c-4310-94c7-f39ceb7500e3/resource/3ed63523-ff9c-41f6-a6fe-980f3d9e501f/download/amministrazioni.txt)
- Better folder structure
- Added missing license header and authors to each file

## 2022/02/13
### \_Zaizen\_
- Scripts now accept an optional date parameter to say where to read/write things.

### Naif
- Updated manual

## 2022/02/14
### \_Zaizen\_
- Updated PROGRESS.md to have information from the beginning of the project too and a current status section to see what we've done and what is missing.
- Docker container (doesn't work)

## 2022/02/18
### \_Zaizen\_
- Check that GA was found
- Enti.tsv path instead of date

### Shamar
- Auto-accept cookies (thanks Mauro Gorrino)

## 2022/04/11
### \_Zaizen\_
- Export JSON from point3

## 2022/04/11
### \_Zaizen\_
- Send PEC mail successfully

## 2022/05/16
### \_Zaizen\_
- Docker environment properly working.

## 2022/05/17
### \_Zaizen\_
- Generate GA_General, a graph showing how many PA's use GA over time

## 2022/05/21
### Shamar
- Documented the new architecture of the observatory (see [ARCHITECTURE.md](./ARCHITECTURE.md))

# Current status

## Folder structure

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
