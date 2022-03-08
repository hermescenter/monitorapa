#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import sys
import requests
import commons

outDir = commons.computeOutDir(sys.argv)
url = 'https://indicepa.gov.it/ipa-dati/datastore/dump/d09adf99-dc10-4349-8c53-27b1e5aa97b6?bom=True&format=tsv'
r = requests.get(url, allow_redirects=True)
result = r.content.replace(
    b'HTTPS:SISTEMAAMBIENTELUCCA.IT', b'HTTPS://SISTEMAAMBIENTELUCCA.IT')
open("%s/enti.tsv" % outDir, 'wb').write(result)
print("%s/enti.tsv" % outDir)
