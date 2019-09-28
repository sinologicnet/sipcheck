#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    sipCheck v.3.0
    ---------------------------
    Script que analiza el /var/log/asterisk/security con la información de seguridad de acceso y registros para bloquear las IPs de los atacantes.
    El funcionamiento es muy sencillo:
        - Si Asterisk detecta un intento de autentificación fallido, lo vuelca al archivo security.log
        - Si Asterisk detecta un intento de autentificación correcto,lo vuelca al archivo security.log

        Si el número de intentos fallidos de una IP supera el valor de "maxNumTries" y esa IP no está en la lista blanca, lo banea.
        Si esa IP se autentifica correctamente alguna vez, puede ser de un cliente y lo mete en la lista blanca para evitar banearlo nuevamente.
        Al cabo de "BLExpireTime" segundos, se elimina esa IP de la lista negra para no llenar la lista de ips que no sirven.
        Al cabo de "WLExpireTime" segundos, se elimina esa IP de la lista blanca para no llenar la lista de ips que no sirven.
        Por lo general, BLExpireTime debería ser menor que WLExpireTime.

'''

import time
import io
import os
import time
import socket
import logging
import asyncio
from panoramisk import Manager
from threading import Thread
from threading import RLock

#######################################################################################################
# Configuration variables
#######################################################################################################

# Asterisk manager configuration
managerHost = "127.0.0.1"           # Manager IP Address
managerPort = 5038                  # Manager port
managerUser = "manageruser"         # Manager user
managerPass = "SuPeR@p4ssw0rd123"   # Manager password

# Logging configuration
logLevel = "DEBUG"           # One of this possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL
logFile = "/var/log/sipcheck.log"   # Filename to dump the events and the actions

# Maximun number of wrong passwords before to insert into the blacklist
maxNumTries = 3

# Number of seconds to expire the record into each list
BLExpireTime = 1*60         # Time in seconds that one IP address will be holded into the blacklist
WLExpireTime = 1*60         # Time in seconds that one IP address will be retained as a friend to trust
TLExpireTime = 1*30         # Time in seconds that one IP address will be holded as a suspected of attack


# Chain of IPTables that will be used to DROP or ACCEPT the attackers or friends addresses.
iptablesChain = "INPUT"     




#######################################################################################################
# Code
#######################################################################################################

lock = RLock()

# We connect into a Asterisk Manager (Asterisk 11 or newer with Security permissions to read)
manager = Manager(loop=asyncio.get_event_loop(), host=managerHost, port=managerPort, username=managerUser, secret=managerPass)

# Set the logging system to dump everything we do
logging.basicConfig(filename=logFile,level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s')
Log = logging.getLogger()
level = logging.getLevelName(logLevel)
Log.setLevel(level)

# We set the lists where we storage the addresses.
templist={}             # Suspected addresses
whitelist={}            # Trusted addresses
blacklist={}            # Attackers addresses


## Function that counts the tries and insert the address into the suspected list.
def templist_counter(ip):
    if (ip not in whitelist) and (ip not in blacklist):
        if (ip in templist):
            templist[ip]['intentos']=templist[ip]['intentos']+1
        else:
            templist[ip]={'intentos':1,'time':int(time.time())}
        output=templist[ip]['intentos']
    else:
        logging.warning("Detected wrong password for "+ip+" but this address is whitelisted.")
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
def insert_to_blacklist(ip):
    if ip not in [y for x in blacklist for y in x.split()]:
        logging.info("BL: Detect attack from IP: '"+ip+"' (more than "+str(maxNumTries)+" wrongs passwords)")
        blacklist[ip]=int(time.time());      # Insert the address and the time into the blacklist
        ban(ip)
        if (ip in templist):    # Remove from suspected list (to save memory)
            templist.pop(ip, None)



## Function that is executed when an 'invalidPassword' is received
def invalidPassword(evento):
    logging.debug("Received wrong password for user "+evento['AccountID']+" from IP "+evento["RemoteAddress"]);
    # We check if the IP address is in the whitelist
    # If it isn't into the whitelist, we increment the counter until the number of tries will be greater that the 'maxNumTries' constant
    num = templist_counter(evento['RemoteAddress'])
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
        if (salida == "127.0.0.1"): # We do nothing with loopback ip
            salida = ""
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
    logging.debug(message)
    successfulAuth(message)

## It register the manager event that warning when the user send a wrong authentication
@manager.register_event('InvalidPassword')
def callback(manager, message):
    message['RemoteAddress']=getIP(message.RemoteAddress.replace('"',''))
    logging.debug(message)
    invalidPassword(message)



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
                    insert_to_whitelist(content,time.time()+(60*60*24*365))
                    unban(content)  # If this address has been banned sometime, we try to remove this ban
                line = fp.readline()
                cnt += 1

## Main function
def main():
    logging.info('-----------------------------------------------------')
    logging.info('Starting SIPCheck 3 ...')
    load_whitelist_file()
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
