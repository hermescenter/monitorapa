#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import time
import sys
import os.path

def usage():
    print("""
./cli/point3.py 

Will create out/YYYY-MM-DD/google_analytics/point3/enti.tsv
""")
    sys.exit(-1)

def getDate(fname):
    return time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(fname)))
def getTime(fname):
    return time.strftime("%H:%m:%S", time.gmtime(os.path.getctime(fname)))

def getFields(lineNum):
    fname = "out/%s.OK.txt" % lineNum
    try:
        with open(fname, 'r') as f:
            content = f.read()
        if len(content) > 0:
            return (1, content, getDate(fname), getTime(fname))
        else:
            return (0, '', getDate(fname), getTime(fname))
    except:
        fname = "out/%s.ERR.txt" % lineNum
        if os.path.exists(fname):
            return (0, '', getDate(fname), getTime(fname))
        return (0, '', '', '')

def main(argv):
    if len(argv) != 1:
        usage()
    count = 0
    with open('amministrazioni.txt', 'r') as inf, open('point3.amministrazioni.txt', 'w') as outf:
        for line in inf:
            outf.write(line[:-1])
            if count == 0:
                outf.write("\tweb_test_result\tweb_test_metadata\tweb_test_date\tweb_test_time\n")
            else:
                outf.write("\t%s\t%s\t%s\t%s\n" % getFields(count))
            count += 1
#            if count > 120:
#                break

if __name__ == "__main__":
    main(sys.argv)


