#!/usr/bin/python

import os, sys, re, operator, string, time, gzip, pprint

from datetime import datetime

def parse_geneious_log(filename):

    if not os.path.isfile(filename):
        print "User file [%s] not found" % filename
        return

    file   = open(filename,'r')
    flines = file.readlines()

    ts = re.compile('TIMESTAMP +(\d+)/(\d+)/(\d+)');
    #us = re.compile('^(\d+):(\d+):(\d+).*OUT.*license\" +(\S+)\@(.*?)\.(\S+)');
    us = re.compile('^ *(\d+):(\d+):(\d+).*OUT.*license\" +(\S+)\@(.*)');
    in_line = re.compile('^ *(\d+):(\d+):(\d+).*IN.*license\" +(\S+)\@(.*)');

    #15:46:26 (geneious) DENIED: "floating_license" James@ham  (Users are queued for this feature. (-24,332))
    den_line = re.compile('^ *(\d+):(\d+):(\d+).*DENIED.*license\" +(\S+)\@(.*) +');

    mon  = "";
    day  = "";
    year = "";

    users     = {}
    usertimes = {}

    timeslice = {}
    tscount   = {}
    
    counts = 0
    dencounts = 0
    
    for line in flines:

        m1 = ts.search(line)
        m2 = us.search(line)
        m3 = in_line.search(line)
        m4 = den_line.search(line)
        
        if m1 and m1.group(3):
            mon  = m1.group(1)
            day  = m1.group(2)
            year = m1.group(3)

        if m3 and m3.group(5):
            user = m3.group(4)
            add  = m3.group(5)
            hrs  = m3.group(1)
            mns  = m3.group(2)
            sec  = m3.group(3)

            counts = counts - 1


        if m4 and m4.group(5):
            user = m4.group(4)
            add  = m4.group(5)
            hrs  = m4.group(1)
            mns  = m4.group(2)
            sec  = m4.group(3)

            print "DENIED %s-%s-%s_%s %s %s"%(year,mon,day,hrs,user,add)
            
        if m2 and m2.group(5):

            user = m2.group(4)
            add  = m2.group(5)
            hrs  = m2.group(1)
            mns  = m2.group(2)
            sec  = m2.group(3)

            counts = counts + 1
            
            if users.has_key(user) == False:
                users[user] = {}

            if users[user].has_key(add) == False:
                users[user][add] = 0

            users[user][add] = users[user][add] + 1

            if mon != "":
                time    = datetime(int(year),int(mon),int(day),int(hrs),int(mns),int(sec))

                if usertimes.has_key(user) == False:
                    usertimes[user] = {}

                usertimes[user][len(usertimes[user])] = time

                mns = int(mns)/30
                mns = mns*30
                time_30minslice = datetime(int(year),int(mon),int(day),int(hrs),mns,0)

                if hrs not in timeslice:
                    timeslice[hrs] = 0
                    tscount[hrs] = 0

                timeslice[hrs] += counts
                tscount[hrs] += 1
                
                print "%s\t%s\t%s\t%s\t%d"%(time,time_30minslice,user,add,counts)


    for t in timeslice:
        print t,timeslice[t],tscount[t],timeslice[t]/tscount[t]
        
    for u in users.keys():
        astr = "";
        count = 0;
        for add in users[u].keys():
            astr = astr + add + " " + str(users[u][add]) + " "
            count = count + users[u][add]

            #print "%25s\t%5d\t%s"%(u,count,astr)

    for u in usertimes.keys():
        first = usertimes[u][0].strftime("%m/%d/%y")
        last  = usertimes[u][len(usertimes[u])-1].strftime("%m/%d/%Y")
       # print "%25s\t%25s\t%25s"%(u,first,last)

def help():
    print "\nParses geneious logs (/n/RC_Team/iliadlic1/license_logs/geneious.log) and reformats by time and user"

    print "\nUsage: python parse_geneious_log.py <logfile>\n\n"

if __name__ == '__main__':

    if len(sys.argv) != 2:
        help()
        sys.exit(0)

    filename = sys.argv[1]

    parse_geneious_log(filename)
  
