#!/usr/bin/env python3
import requests
url = 'https://indicepa.gov.it/ipa-dati/dataset/502ff370-1b2c-4310-94c7-f39ceb7500e3/resource/3ed63523-ff9c-41f6-a6fe-980f3d9e501f/download/amministrazioni.txt'
r = requests.get(url, allow_redirects=True)
open('amministrazioni.txt', 'wb').write(r.content)

