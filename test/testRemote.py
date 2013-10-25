#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import subprocess

x=raw_input("What is your IP address? ")

def ipformatcheck(x):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, x):
        #return True
        print ("Ip format valid")
        #print (‘Reversing the IP’)
        ip = str(x).split('.')
        rev = '%s.%s.%s.%s' % (ip[3],ip[2],ip[1],ip[0])
                spamdbs = ['.dnsbl.sorbs.net', '.cbl.abuseat.org', '.bl.spamcop.net', '.zen.spamhaus.org', '.sbl.spamhaus.org', '.xbl.spamhaus.org', '.pbl.spamhaus.org']
                for db in spamdbs:
                       if db == ".pbl.spamhaus.org":
                           break
                       p = subprocess.Popen(["dig", "+short", rev+db], stdout=subprocess.PIPE)
                       output, err = p.communicate()
                       print db
                       print output
        else:
        #return False
        print ("IP format InValid")

ipformatcheck(x)
