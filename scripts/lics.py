#!/usr/bin/env python

# Using the geneious_license_count file, this matches the simultaneous license count
# with the time stamp and generates a table
import os, re, dateutil, sys

def main(argv):
    
    if len(argv) < 2:
	raise Exception("Need a file argument")
    
    cntfile = argv[1]
    print "Processing %s" % cntfile
    if not os.path.isfile(cntfile):
        raise Exception("File %s is not a file." % cntfile)
    
    data = []
    timelinere = re.compile("Flexible License Manager status on (.*)")
    liclinere  = re.compile("Total of (\d+) licenses in use")
    try:
        timeval = None
        liccount = 0
        with open(cntfile,'r') as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                m = timelinere.match(line)
                if m:
                    timeval = m.group(1)
                    liccount = 0
                m = liclinere.search(line)
                if m:
                    liccount = int(m.group(1))
                    print '%s\t%d' % (timeval, liccount)
        return 0
    except Exception as e:
        sys.stderr.writeln(str(e) + '\n')
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))


