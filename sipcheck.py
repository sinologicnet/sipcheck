#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    sipCheck v.3.0
    ---------------------------
    This application connects into the Asterisk Manager Interface (v11 or newer) and reads the Security Events received when some user try send
    INVITE or REGISTER and when it happens SIPCheck classify the IP address into 'friends' or, if the user continues sending wrong passwords, 
    into 'attackers'.
    
    SIPCheck counts the number of failed tries per IP Address so, if this address is not into a white list, and the tries are exceeded the limits
    automatically will be baned during some time.

    The new purpous of this application is ban attackers and automatically clean the IP past some time to avoid the firewall be bigger and bigger

    If some IP address auth correctly, it is consider a "friend who trust" and it will be classified into white list to avoid be banned although
    some SIP client send wrong passwords. (maybe this SIP users belongs a company with some phones and one of them are badly configured).

    You can find more information at: 
        https://github.com/sinologicnet/sipcheck

    If you have questions or suggestions, you can use this page: 
        https://github.com/sinologicnet/sipcheck/issues

    Authors: 
        Elio Rojano, Sergio Cotelo, Javier Vidal, Tomás Sahagún
    
    Email: 
        sipcheck@sinologic.net

'''

import time
import io
import os
import time
import socket
import logging
import asyncio
import configparser
from panoramisk import Manager
from threading import Thread
from threading import RLock

lock = RLock()

# We parser the config file
config = configparser.ConfigParser()
config.read('sipcheck.conf')

if ('manager' in config):
    managerHost = config['manager']['host']
    managerPort = int(config['manager']['port'])
    managerUser = config['manager']['username']
    managerPass = config['manager']['password']
else:
    managerHost = "127.0.0.1"
    managerPort = 5038
    managerUser = "manageruser"
    managerPass = "SuPeR@p4ssw0rd123"

if ('log' in config):
    logLevel = config['log']['level']
    logFile = config['log']['file']
else:
    logLevel = "DEBUG"          
    logFile = "/var/log/sipcheck.log"

if ('attacker' in config):
    maxNumTries = int(config['attacker']['maxNumTries'])
    BLExpireTime = int(config['attacker']['BLExpireTime'])
    WLExpireTime = int(config['attacker']['WLExpireTime'])
    TLExpireTime = int(config['attacker']['TLExpireTime'])
    iptablesChain = config['attacker']['iptablesChain']
else:
    maxNumTries = 5
    BLExpireTime = 86400
    WLExpireTime = 21600
    TLExpireTime = 3600
    iptablesChain = "INPUT"



# We connect into a Asterisk Manager (Asterisk 11 or newer with Security permissions to read)
manager = Manager(loop=asyncio.get_event_loop(), host=managerHost, port=managerPort, username=managerUser, secret=managerPass)

# Set the logging system to dump everything we do
logging.basicConfig(filename=logFile,level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s')
Log = logging.getLogger()
level = logging.getLevelName(logLevel)
Log.setLevel(level)


logging.debug("Configured Blacklist expire time: "+str(BLExpireTime))
logging.debug("Configured Whitelist expire time: "+str(WLExpireTime))
logging.debug("Configured Templist expire time: "+str(TLExpireTime))



# We set the lists where we storage the addresses.
templist={}             # Suspected addresses
whitelist={}            # Trusted addresses
blacklist={}            # Attackers addresses


## Function that counts the tries and insert the address into the suspected list.
def templist_counter(ip,how=1.0):
    if (ip not in whitelist) and (ip not in blacklist):
        if (ip in templist):
            templist[ip]['intentos']=templist[ip]['intentos']+how
        else:
            templist[ip]={'intentos':how,'time':int(time.time())}
        output=templist[ip]['intentos']
    elif (ip in whitelist):
        logging.warning("Detected wrong password for "+ip+" but this address is whitelisted.")
        output=0
    else:   # It shouldn't happen
        logging.warning("Detected wrong password for "+ip+" but this address is blacklisted.")
        output=0
    return output

## Function that insert the rule to drop everything from the ip into the iptables
def ban(ip):
    if (not isbanned(ip)):
        logging.info("Banned IP: "+ip)
        myCmd = os.popen("iptables -A "+iptablesChain+" -s "+ip+" -j DROP").read()

## Function that delete the rule to drop everything from the ip into the iptables
def unban(ip):
    if (isbanned(ip)):
        logging.info("Unbaned IP: "+ip)
        myCmd = os.popen("iptables -D "+iptablesChain+" -s "+ip+" -j DROP").read()

##  Returns if an IP Address is the iptables list
def isbanned(ip):
    Out=os.popen("iptables -L "+iptablesChain+" -n").read().replace(" ","#").replace("\n","")
    out=False
    if ("#"+ip+"#" in Out): # we uses '#' to sure that we don't confuse with pieces of others ip addresses
        out=True
    return out

def create_blackfile():
    f = open("/tmp/blacklist.dat", "w")
    f.write("# This file is generated automatically by SIPCheck 3, so please, dont modify it\n\n")
    for t in blacklist:
        f.write(t+","+str(blacklist[t])+"\n")
    f.close()


## Function that add an IP address into a whitelist (and remove from list of suspected)
def insert_to_whitelist(ip,hastacuando=time.time()):
    if ip not in [y for x in whitelist for y in x.split()]:
        whitelist[ip]=int(hastacuando)    # Insert into the whitelist
        if (ip in templist):    # Extract from suspected list (to save memory)
            templist.pop(ip, None)
        # note: I know that we should haven't this ip address into the blacklist, but if it happen, we remove too. ;)
        if (ip in blacklist):
            blacklist.pop(ip, None)

## Function that add an IP address into a blacklist (and remove from list of suspected)
def insert_to_blacklist(ip,cuando=time.time()):
    if ip not in [y for x in blacklist for y in x.split()]:
        logging.info("BL: Detect attack from IP: '"+ip+"' (more than "+str(maxNumTries)+" wrongs passwords)")
        blacklist[ip]=int(cuando);      # Insert the address and the time into the blacklist  
        ban(ip)
        create_blackfile()
        if (ip in templist):    # Remove from suspected list (to save memory)
            templist.pop(ip, None)



## Function that is executed when an 'invalidPassword' is received
def invalidPassword(evento):
    logging.debug("Received wrong password for user "+evento['AccountID']+" from IP "+evento["RemoteAddress"]);
    # We check if the IP address is in the whitelist
    # If it isn't into the whitelist, we increment the counter until the number of tries will be greater that the 'maxNumTries' constant
    num = templist_counter(evento['RemoteAddress'],1.0)
    if (num > maxNumTries):
        insert_to_blacklist(evento['RemoteAddress'])

## Function that is executed when an 'invalidPassword' is received
def inviteSend(evento):
    logging.debug("Received invite user "+evento['AccountID']+" from IP "+evento["RemoteAddress"]);
    # We check if the IP address is in the whitelist
    # If it isn't into the whitelist, we increment the counter until the number of tries will be greater that the 'maxNumTries' constant
    num = templist_counter(evento['RemoteAddress'],0.4)
    if (num > maxNumTries):
        insert_to_blacklist(evento['RemoteAddress'])


## Function that is executed when an 'successfulAuth' is received
def successfulAuth(evento):
    logging.debug("Received right password for user "+evento['AccountID']+" from IP "+evento["RemoteAddress"]);
    # We insert the IP address into the whitelist
    insert_to_whitelist(evento['RemoteAddress'])


## Function to filter the string with IPv4 IP address from the manager object and returns just the IP address.
def getIP(stringip):
    ## We get the string "IPV4/UDP/X.X.X.X/5062" and we need only "X.X.X.X"
    paramsIP=stringip.strip().split("/")
    salida="";
    if (len(paramsIP) > 3):
        salida=paramsIP[2]
    return salida

## Returns if a string is a valid IP address
def isValidIP(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False
    return True



## Function that go through the lists checking the time when the addresses was inserted and if this time is greater than the Expiretime configured, it removes the addresses of these lists.
def expireRecord():
    now=int(time.time())

    # We search the elements with the time expired.
    listaABorrar=[]
    for t in blacklist:
        if (now - blacklist[t] > BLExpireTime):
            logging.info("BL: Expired time for "+t)
            listaABorrar.append(t)
    # ... and we remove the elements found
    for t1 in listaABorrar:
        blacklist.pop(t1, None)
        unban(t1)       # Lo extraemos del firewall

    # We search the elements with the time expired.
    listaABorrar=[]
    for t in whitelist:
        if (now - whitelist[t] > WLExpireTime):
            logging.info("WL: Expired time for "+t)
            listaABorrar.append(t)
    # ... and we remove the elements found
    for t1 in listaABorrar:
        whitelist.pop(t1, None)

    # We search the elements with the time expired.
    listaABorrar=[]
    for t in templist:
        if (now - templist[t]['time'] > TLExpireTime):
            logging.info("TL: Expired time for "+t)
            listaABorrar.append(t)
    # ... and we remove the elements found
    for t1 in listaABorrar:
        templist.pop(t1, None)

    
    # Uncomment this block to see updately the content of the lists (only for development)
    if (logLevel == "DEBUG"):
        print("blacklist "+str(blacklist))
        print("whitelist "+str(whitelist))
        print("templist "+str(templist))
    

## Function that execute "expireRecord" function each 5 seconds
def expire():
    while True:
        logging.debug("Executing expire process...")
        expireRecord()  # We process the lists to remove the expired records
        time.sleep(5)




## It register the manager event that warning when the user send a right authentication
@manager.register_event('SuccessfulAuth')
def callback(manager, message):
    message['RemoteAddress']=getIP(message.RemoteAddress.replace('"',''))
    if (message['RemoteAddress'] != "127.0.0.1"):
        logging.debug(message)
        successfulAuth(message)

## It register the manager event that warning when the user send a wrong authentication
@manager.register_event('InvalidPassword')
def callback(manager, message):
    message['RemoteAddress']=getIP(message.RemoteAddress.replace('"',''))
    logging.debug(message)
    invalidPassword(message)

## It register the manager event that warning when the user send a wrong authentication
@manager.register_event('ChallengeSent')
def callback(manager, message):
    message['RemoteAddress']=getIP(message.RemoteAddress.replace('"',''))
    logging.debug(message)
    inviteSend(message)



## Function that insert the addresses located in whitelist.txt file, into the whitelist without expiretime.
def load_whitelist_file():  
    wlfile="./whitelist.txt"
    logging.debug("Reading "+wlfile+" to insert IP address into Whitelist table...")
    if (os.path.exists(wlfile)):
        with io.open(wlfile) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                content = line.strip()
                if (content != "") and (content[0] != "#") and (isValidIP(content)):
                    logging.info("+ Added "+content+" into whitelist during one year")
                    insert_to_whitelist(content,time.time()+(60*60*24*365))
                    unban(content)  # If this address has been banned sometime, we try to remove this ban
                line = fp.readline()
                cnt += 1


## Function that insert the addresses located in blacklist.txt file, into the blacklist (and ban them again if they wasn't on the iptables).
# If the time when they was banned is greater than BLExpireTime, the thread of ExpireTime will remove this address again.
def load_blacklist_file():  
    blfile="/tmp/blacklist.dat"
    logging.debug("Reading "+blfile+" to insert IP address into Blacklist table...")
    if (os.path.exists(blfile)):
        with io.open(blfile) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                content = line.strip()
                if (content != "") and (content[0] != "#"):
                    registro = content.split(",")                     
                    if (len(registro) == 2) and (isValidIP(registro[0])):
                        logging.info("+ Added "+content+" into blacklist again from the time: "+str(registro[1]))
                        insert_to_blacklist(registro[0],registro[1])
                line = fp.readline()
                cnt += 1


## Main function
def main():
    logging.info('-----------------------------------------------------')
    logging.info('Starting SIPCheck 3 ...')
    load_whitelist_file()
    load_blacklist_file()
    manager.connect()
    try:
        # We create an asyncronous thread that check the expiretime of the lists
        Thread(name='expireRecord', target = expire).start()
        # Run the manager loop
        manager.loop.run_forever()
    except KeyboardInterrupt:
        manager.loop.close()

if __name__ == '__main__':
    main()
