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

# Current status

## Folder structure

```
monitorapa
│   README.md
│   PROGRESS.md
│   LICENCE.txt
│   AUTHORS.md
│   .gitignore
│
└───check
│   │   google_analytics.js
│
└───cli
│   │   MANUAL.md
│   │   SPECIFICATION.md
│   │   commons.py
│   │   point1.py
│   │   point2.py
│   │   point3.py
│   │   point4.py
│   │   point4_sample.cfg
│   │   requirements.txt
│
└───out
│   │   .gitkeep
```

## Point1

- Downloads a [tsv file](https://indicepa.gov.it/ipa-dati/datastore/dump/d09adf99-dc10-4349-8c53-27b1e5aa97b6?bom=True&format=tsv) containing various details of italian PAs to then save in a folder inside [out/](https://github.com/hermescenter/monitorapa/tree/main/out) named after the date of download

## Point2

- Can scan all the PAs sites for google_analytics presence and report it in the approriate folder (see [MANUAL.md](https://github.com/hermescenter/monitorapa/blob/main/cli/MANUAL.md)).

## Point3

- Process point2 output and generate a new enti.[format] in the appropriate folder (see [MANUAL.md](https://github.com/hermescenter/monitorapa/blob/main/cli/MANUAL.md)). You can choose the export format between json and tsv (default).

## Folder structure after Point1, Point2 and Point3

The structure is the same except for the [out/](https://github.com/hermescenter/monitorapa/tree/main/out) folder:

```
out
│
└───202?-??-??
│   │   LICENSE.txt
│   │   README.md
│   │   enti.tsv
│   │
│   └───google_analytics
│       │
|       └───point2
|       |   |   1.ERR.txt
|       |   |   2.OK.txt
|       |   |   3.OK.txt
|       |   |   ...
|       |   |   22844.OK.txt
|       |
|       └───point2
|       |   | enti.tsv
|       |
|       └───point4
```

## Point4

- Reads data from point3 and send emails correctly. It doesn't check if all required fields exists yet.

## Point5

- Nothing done yet.
