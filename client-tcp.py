#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Testing control connection with server.
    Simple protocol:
        -login: 
             -send user:password
             -get "ok" from server to continue

        -wait for commands:
             -add ban x.x.x.x
             -del ban x.x.x.x
             -...
             
"""
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send login 
    message = 'user:pass\r\n'
    print >>sys.stderr, 'login on %s port %s' % server_address
    sock.sendall(message)

    # Wait for login confirmation 
    data = sock.recv(1024)
    data = data.replace('\r', '')
    data = data.replace('\n', '')
    print >>sys.stderr, 'received "%s"' % data

    if data == "ok" :
        print >>sys.stderr, 'logged in'
        while True:
            data = sock.recv(1024)
            data = data.replace('\r', '')
            data = data.replace('\n', '')
            print >>sys.stderr, 'received "%s"' % data

            parts = data.split(" ")
            print >>sys.stderr, 'command: "%s"' % parts[0]
            print >>sys.stderr, 'subcommand: "%s"' % parts[1]
            print >>sys.stderr, 'params: "%s"' % parts[2]

            #Processing commands from server:
            if command == "add" :
                print >>sys.stderr, "Add"
           
            elif command == "del" :
                print >>sys.stderr, "Del"

            else:
                print >>sys.stderr, "Bad Command"

    else:
        print >>sys.stderr, 'error on login'
        sock.close()
        sys.exit(1)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

