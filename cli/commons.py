# This file is part of MonitoraPA
#
# Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import datetime
import os
import os.path
import shutil
import sys

README = """
This folder has been created by MonitoraPA on %s.

The file enti.tsv has been created by AgID and distributed under CC BY 4.0.
An updated version can be downloaded from https://indicepa.gov.it/ipa-dati/dataset/enti

Everything else inside this folder can be used under the Hacking License.
See LICENCE.txt for the exact terms and conditions.

"""


def outputReadme(dirName):
    with open(os.path.join(dirName, "README.md"), 'w') as f:
        f.write(README % os.path.basename(dirName))
        f.close()


def computeOutDir(argv):
    if not os.path.isdir("out"):
        sys.exit(
            "Cannot find out/ directory.\n\nPlease run cli/ scripts from the root of the repository.")
    if not os.path.isfile("LICENSE.txt"):
        sys.exit(
            "Cannot find LICENSE.txt.\n\nPlease run cli/ scripts from the root of the repository.")
    if "cli/point1.py" in argv[0]:
        dirName = "out/%s" % datetime.datetime.utcnow().strftime("%Y-%m-%d")
        if not os.path.isdir(dirName):
            os.mkdir(dirName)
            #print("Created output dir %s" % dirName)
        if not os.path.isfile(os.path.join(dirName, "LICENSE.txt")):
            shutil.copy(os.path.abspath("LICENSE.txt"),
                        os.path.abspath(dirName))
        if not os.path.isfile(os.path.join(dirName, "README.md")):
            outputReadme(dirName)
        return dirName

    if not "check/" in argv[1]:
        sys.exit("Missing GDPR compliance check.")

    if not "out/" in argv[2] or not "enti.tsv" in argv[2]:
        sys.exit("Missing enti.tsv path.")

    check = os.path.splitext(os.path.basename(argv[1]))[0]
    outDir = os.path.dirname(argv[2])
    point = os.path.splitext(os.path.basename(argv[0]))[0]

    dirName = "%s/%s/%s" % (outDir, check, point)

    if not os.path.isdir(dirName):
        os.makedirs(dirName, 0o755)
    return dirName
