from argparse  import ArgumentParser

import importlib
import logging
import re
import os
import sys
import csv
import pprint

def main(args):

    file = args.file
    
    #print"Geneious count log File [%s]"%file
    
    daydata   = {}
    daycounts = {}

    monthdata   = {}
    monthcounts = {}

    #Flexible License Manager status on Tue 11/15/2011 13:30
    #Users of floating_license:  (Total of 10000 licenses issued;  Total of 0 licenses in use)
    #Flexible License Manager status on Tue 11/15/2011 14:00
    #Users of floating_license:  (Total of 10000 licenses issued;  Total of 0 licenses in use)
    #Flexible License Manager status on Tue 11/15/2011 14:30
    #Users of floating_license:  (Total of 10000 licenses issued;  Total of 0 licenses in use)

    weekday = None
    month   = None
    day     = None
    year    = None
    hour    = None
    mins    = None
    count   = 0

    with open(file) as fp:

        for line in fp:
           line = line.rstrip('\n')

           match = re.match('^Flexible.*on (\S+) (\d+)\/(\d+)\/(\d\d\d\d) (\d\d):(\d\d)',line)               # Look for an end line

           if match:
               weekday = match.group(1)
               month = int(match.group(2))
               day   = int(match.group(3)) 
               year  = int(match.group(4)) 
               hour  = int(match.group(5)) 
               mins  = int(match.group(6)) 

               day   = str(day).zfill(2)
               month = str(month).zfill(2)

           match = re.match('^Users.*Total of (\d+) +licenses.*',line)                    

           if match:
               count = int(match.group(1))

               #print "Date %s %d %d %d Time %d %d Count %d"%(weekday,year,month,day,hour,mins,count)

           date  = str(year) + "-" + str(month) + "-" + str(day)
           monthdate = str(year) + "-" + str(month)

           if date not in daydata:
              daydata[date] = 0

           if date not in daycounts:
              daycounts[date] = 0

           daydata[date]   = daydata[date] + count
           daycounts[date] = daycounts[date] + 1

           if monthdate not in monthdata:
              monthdata[monthdate] = 0

           if monthdate not in monthcounts:
              monthcounts[monthdate] = 0

           monthdata[monthdate]   = monthdata[monthdate] + count
           monthcounts[monthdate] = monthcounts[monthdate] + 1

    if args.day:
      for key in sorted(daydata):
        print "%s\t%d"%(key,int(daydata[key]/daycounts[key]))

    if args.month:
      for key in sorted(monthdata):
        print "%s\t%d"%(key,int(monthdata[key]/monthcounts[key]))

if __name__ == '__main__':

    parser        = ArgumentParser(description = 'Geneious count log parser')

    parser.add_argument('-f','--file'   , help='The Geneious count log file')
    parser.add_argument('-d','--day'   , help='Print average license usage count in 30 minutes over 1 day',action='store_true')
    parser.add_argument('-m','--month'   , help='Print average license usage count in 30 minutes over 1 month',action='store_true')
    
    args = parser.parse_args()

    #print args

    if args.file is None:
       print "ERROR: No input file set (use -file <myfile>)\n"
       sys.exit()

    if not os.path.isfile(args.file):
       print "ERROR: Input file [%s] doesn't exist\n"%args.file
       sys.exit()

    main(args)

