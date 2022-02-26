#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import sys
import os
import commons

def usage():
    print("""
./cli/point2parallel.py check/test_to_run.js out/yyyy-mm-dd/enti.tsv chunk_size

Executes ./cli/point2.py in a few parallel process of 
chunk_size (must be an integer greater than 100)
""")
    sys.exit(-1)

def main(argv):
    processes = []
    if len(argv) > 4 or len(argv) < 2:
        usage()
    
    test = argv[1]
    if not os.path.isfile(test):
        print("Invalid check to run '%s': file does not exists." % test)
        usage()
    source = argv[2]
    if not os.path.isfile(source):
        print("Invalid path to enti.tsv '%s': file does not exists." % source)
        usage()
    try:
        chunk = int(argv[3])
    except:
        print("Missing or invalid chunk_size (must be an integer)")
        usage()

    if chunk < 100:
        print("Chunk size too small: %s" % chunk)
        usage()
        
    outDir = commons.computeOutDir(argv)

    with open(source, 'r') as s:
        num_lines = sum(1 for line in s)
    
    chunks = num_lines // chunk
    if num_lines % chunk > 0:
        chunks += 1
    
    programToRun = "./cli/point2.py"
    
    for start in range(chunks):
        pid = os.fork()
        if pid == 0:
            new_stdout = os.open("%s/point2.from-%s.pid-%s.txt" % (outDir, (start * chunk), os.getpid()), os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
            os.dup2(new_stdout, 1)
            os.dup2(new_stdout, 2)
            os.execlp("python3", "python3", "-u", programToRun, test, source, "%s" % (start * chunk), "%s" % chunk)
        else:
            print("pid %s: %s %s %s %s %s" % (pid, programToRun, test, source, (start * chunk), chunk))
            processes.append(pid)

    while processes:
        pid, exit_code = os.wait()
        if exit_code//256 != 0:
            print("point2.py at pid %s exited with code %s" % (pid, exit_code//256))
        processes.remove(pid)

if __name__ == "__main__":
    main(sys.argv)
