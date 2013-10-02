"""
    Log badass IPs.

    sqlite: table IPAS(id,ip,try)
    
"""
import time, os

#Set the filename and open the file
filename = 'log.txt'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(0.2)
        file.seek(where)
    else:
        #If line contents "markers" get IP
        if "Wrong password" in line:
            print line.split(" ")[10].split("'")[1].split(":")[0]

        if "rejected" in line:
            print line.split(" ")[8].split("(")[1].split(":")[0]
