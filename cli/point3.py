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
import commons
import json


def usage():
    print("""
./cli/point3.py check/test_to_run.js out/202?-??-??/enti.tsv [format]

Will create out/YYYY-MM-DD/google_analytics/point3/enti.[format] (default format is TSV)

Format options: tsv, json
""")
    sys.exit(-1)


def getDate(fname):
    return time.strftime("%Y-%m-%d", time.gmtime(os.path.getctime(fname)))


def getTime(fname):
    return time.strftime("%H:%m:%S", time.gmtime(os.path.getctime(fname)))


def getFields(lineNum, outDir):
    fname = outDir + "/../point2/%s.OK.txt" % lineNum
    try:
        with open(fname, 'r') as f:
            content = f.read()
        if len(content) > 0:
            if " " in content or "d" in content or "x" in content or "X" in content:
                # website was WAY too slow or GA is somehow misconfigured
                return (0, '', getDate(fname), getTime(fname))
            return (1, content, getDate(fname), getTime(fname))
        else:
            return (0, '', getDate(fname), getTime(fname))
    except:
        fname = outDir + "/../point2/%s.ERR.txt" % lineNum
        if os.path.exists(fname):
            return (0, '', getDate(fname), getTime(fname))
        return (0, '', '', '')


def process_tsv(inf, outf, outDir):
     count = 0
     for line in inf:
            outf.write(line[:-1])
            if count == 0:
                outf.write(
                    "\tweb_test_result\tweb_test_metadata\tweb_test_date\tweb_test_time\n")
            else:
                outf.write("\t%s\t%s\t%s\t%s\n" % getFields(count, outDir))
            count += 1


def process_json(inf, outf, outDir):
    result = {}
    count = 0
    fields_names = []
    for line in inf:
        fields = line.split('\t')
        if count == 0 :
            fields_names = fields
        else:    
            result[fields[1]] = {}
            index = 0
            for field_name in fields_names:
                result[fields[1]][field_name] = fields[index]
                index += 1
            
            extra_fields = getFields(count, outDir)
            result[fields[1]]["web_test_result"] = extra_fields[0]
            result[fields[1]]["web_test_metadata"] = extra_fields[1]
            result[fields[1]]["web_test_date"] = extra_fields[2]
            result[fields[1]]["web_test_time"] = extra_fields[3]
            
        count += 1
    
    outf.write(json.dumps(result))


def main(argv):
    if len(argv) > 4:
        usage()

    outDir = commons.computeOutDir(sys.argv)
    print(outDir)

    format = "tsv"

    if argv[3]:
        if argv[3] != "json" and argv[3] != "tsv":
            usage()
        format = argv[3]

   
    with open(argv[2], 'r') as inf, open(outDir + '/enti.'+format, 'w') as outf:
        globals()['process_'+format](inf, outf, outDir)


if __name__ == "__main__":
    main(sys.argv)
