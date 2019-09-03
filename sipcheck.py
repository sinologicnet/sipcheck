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
import requests
import logging
from threading import Thread
from threading import RLock

lock = RLock()

# Número máximo de peticiones de contraseña inválidas antes de meterlo en la lista negra
maxNumTries = 3

# Número de segundos en el que un registro expirará de la lista
BLExpireTime = 10*60       # Blacklist
WLExpireTime = 10*60       # Whitelist

# Configuramos el archivo donde vamos a guardar los cambios
logging.basicConfig(filename='/var/log/sipcheck.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s: %(message)s')

## Lista de sospechosos
## Cada vez que se recibe un fallo de contraseña se añade (si no está en la lista blanca) la IP a la lista de sospechosos
## y cuando llega a X fallos seguidos, se bloquea (añadiéndolo a la lista negra)
templist={}             ## lista de sospechosos que lleva el número de fallos de una IP

## Lista blanca
## Es la lista de las IPs que han confirmado que son clientes con alguna contraseña válida.
## De esta manera evitamos meter en la lista negra a un cliente que ya esté funcionando.
whitelist={}

## Lista negra
## Es la lista de los sospechosos que han fallado X contraseñas seguidas.
## Debería estar sincronizado con IPTables para bloquear por red la IP atacante.
## Una IP en la lista negra debe caducar por defecto a las 24 horas (ya que normalmente atacan desde ips vulnerables y proxys)
blacklist={}


## Función que incrementa el contador de fallos a la vez que lo insertamos en la lista de sospechosos.
def contador_tempList(ip):
    if (ip not in whitelist) and (ip not in blacklist):
        if (ip in templist):
            templist[ip]=templist[ip]+1
        else:
            templist[ip]=1
        output=templist[ip]
    else:
        output=0
    return output


## Función que añade una IP a la lista blanca (y la saca de la lista de sospechosos)
def anadir_IP_a_listaBlanca(ip):
    if ip not in [y for x in whitelist for y in x.split()]:
        whitelist[ip]=int(time.time())    # Lo añadimos a la lista blanca
        if (ip in templist):    # Lo sacamos de la lista de sospechosos (para ahorrar memoria)
            templist.pop(ip, None)
        # No deberíamos tenerlo en la lista negra (ya que al estar bloqueado, no podría enviar una contraseña correcta) pero aún así, lo vamos a intentar
        if (ip in blacklist):
            blacklist.pop(ip, None)


## Función que añade una IP a la lista negra (y la saca de la lista de sospechosos)
def anadir_IP_a_listaNegra(ip):
    if ip not in [y for x in blacklist for y in x.split()]:
        blacklist[ip]=int(time.time());      # anadimos a la lista negra y apuntamos cuando lo hemos añadido.
        if (ip in templist):    # Lo sacamos de la lista de sospechosos (para ahorrar memoria)
            templist.pop(ip, None)


## Función que se ejecuta cuando se recibe un "invalidPassword" (usuario o contraseña incorrecta)
def invalidPassword(evento):
    logging.debug("Received wrong password for user "+evento['AccountID']+" from IP "+evento["RemoteAddress"]);
    # Comprobamos si la IP pertenece a una IP en la lista blanca
    # Si no está en la lista blanca, incrementamos el contador hasta que el número de peticiones supere la cantidad máxima
    num = contador_tempList(evento['RemoteAddress'])
    if (num > maxNumTries):
        anadir_IP_a_listaNegra(evento['RemoteAddress'])


## Función que se ejecuta cuando se recibe un "successfulAuth" (contraseña correcta)
def successfulAuth(evento):
    logging.debug("Received right password for user "+evento['AccountID']+" from IP "+evento["RemoteAddress"]);
    # La añadimos a la lista blanca
    anadir_IP_a_listaBlanca(evento['RemoteAddress'])


## Función para filtrar la cadena donde viene la IP y devolver la IP real.
def getIP(stringip):
    ## Recibimos IPV4/UDP/X.X.X.X/5062 y queremos obtener X.X.X.X
    paramsIP=stringip.strip().split("/")
    salida="";
    if (len(paramsIP) > 3):
        salida=paramsIP[2]
    return salida


# Función para procesar cada línea que pasamos por parámetro y extraer los campos que nos interesa
def process(line):
    campos = line.strip().split("res_security_log.c:")
    if (len(campos) > 1):
        listaCampos = campos[1].split(",")
        evento={}
        for campovalor in listaCampos:
            keyvalue=campovalor.split("=")
            keyvalue[0]=keyvalue[0].strip()
            keyvalue[1]=keyvalue[1].strip()
            if (keyvalue[0] == "RemoteAddress"):
                keyvalue[1] = getIP(keyvalue[1].replace('"',''))
            evento[keyvalue[0]] = keyvalue[1].replace('"','')

        #print(evento)

        # Ya tenemos el evento... ahora toca analizarlo
        if (evento["SecurityEvent"] == "InvalidPassword"):      # Se ha recibido una contraseña inválida. (comprobamos si la ip está en la lista blanca y si no, lo inscribimos en la lista de los niños malos)
            invalidPassword(evento)
        elif (evento["SecurityEvent"] == "SuccessfulAuth"):     # Contraseña acertada, lo sacamos de la lista de los niños malos (si estuviera) y lo apuntamos a la lista blanca.
            successfulAuth(evento)

        ## Imprimimos las listas
        '''
        print("TempList")
        print(templist)
        print("WhiteList")
        print(whitelist)
        print("BlackList")
        print(blacklist)
        '''

## Función que recorre las listas buscando registros antiguos y eliminando aquellos que llevan más tiempo del conveniente (variable expireTime)
## De esta forma evitamos tener en memoria cientos de registros
## Primero seleccionamos los elementos a borrar y luego se borran, porque de borrarlos directamente da un RuntimeError: "dictionary changed size during iteration"
def expireRecord():
    now=int(time.time())

    ## Seleccionamos la lista de elementos caducados en función del tiempo que llevan
    listaABorrar=[]
    for t in blacklist:
        if (now - blacklist[t] > BLExpireTime):
            logging.info("BL: Expire time for "+t)
            listaABorrar.append(t)
    ## Y las borramos
    for t1 in listaABorrar:
        blacklist.pop(t1, None)

    ## Seleccionamos la lista de elementos caducados en función del tiempo que llevan
    listaABorrar=[]
    for t in whitelist:
        if (now - whitelist[t] > WLExpireTime):
            logging.info("BL: Expire time for "+t)
            listaABorrar.append(t)
    ## Y las borramos
    for t1 in listaABorrar:
        whitelist.pop(t1, None)

    '''
    print("blacklist "+str(blacklist))
    print("whitelist "+str(whitelist))
    print("templist "+str(templist))
    '''
## Comienzo de la función principal
def parseLog():
    global blacklist,whitelist,templist
    f = open('/var/log/asterisk/security', 'r')             ## Abrimos el archivo /var/log/asterisk/security (que previamente hemos habilitado en /etc/asterisk/logger.conf)
    f.seek(0, io.SEEK_END)                                  ## Nos vamos al final del fichero y empezamos a analizar los cambios
    while True:
        line = ''
        while len(line) == 0 or line[-1] != '\n':           ## Analizamos cada línea nueva que vaya apareciendo en el archivo
            tail = f.readline()
            if tail == '':
                time.sleep(0.1)
                continue
            line += tail
        process(line.strip())                               ## Por cada línea, la enviamos a 'process' para procesarla y ver si nos interesa o no.

## Comienzo del sistema de caducidad de registros (para evitar que haya registros permanentemente)
def expire():
    while True:
        expireRecord()                                      ## Procesamos las listas para eliminar aquellos registros que han expirado
        time.sleep(5)

## Llamamos de forma asíncrona a las dos funciones para que cada una trabaje a su ritmo.
logging.info('Starting SIPCheck3...')
Thread(name='parseLog', target = parseLog).start()
Thread(name='expireRecord', target = expire).start()

