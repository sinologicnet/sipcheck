#!/usr/bin/env python

import SocketServer, sys, time, base64 
from threading import Thread

HOST = '0.0.0.0'
PORT = 6969 

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        code  = self.hashcode()
        user  = None
        login = False

        while True:
            reply = None
            data  = None
            
            try:
                data  = self.request.recv(1024)
                data  = data.replace('\r', '')
                data  = data.replace('\n', '')
            except:
                pass

            if data == "HELO" or data == "EHLO":
                reply = "HELO " + code + "\n"

            elif "PING" in data:
                if " " in data: 
                    coderecv = data.split(" ")[1]

                    if coderecv == code:              
                        reply = "PONG " + code + "\n"
                
                    else:
                        self.request.send("ERROR: BAD PING!\n")
                        self.request.close()
                        break
                else:
                    self.request.send("ERROR: BAD PING!\n")
                    self.request.close()
                    break

            elif "QUIT" in data or "EXIT" in data:
                self.request.send("BYE BYE!\n")
                self.request.close()
                break

            elif "USER"  in data:
                if " " in data:
                    coderecv = data.split(" ")[1]

                    if coderecv == code:
                        user = data.split(" ")[2]

                    else:
                        self.request.send("ERROR: BAD COMMAND!\n")
                        self.request.close()
                        break
                else:
                    self.request.send("ERROR: BAD COMMAND!\n")
                    self.request.close()
                    break

            elif "PASS" in data and user is not None:
                if " " in data:
                    coderecv = data.split(" ")[1]
                    passw    = data.split(" ")[2]

                    if coderecv == code:
                        #Comprobar user/pass
                        reply = "OK " + code + " " + user + "\n"
                        login = True

                    else:
                        self.request.send("ERROR: BAD COMMAND!\n")
                        self.request.close()
                        break
                else:
                    self.request.send("ERROR: BAD COMMAND!\n")
                    self.request.close()
                    break

            elif "GET" in data:
                if login == True:
                    if " " in data:
                        coderecv = data.split(" ")[1]
 
                        if coderecv == code:
                            reply = "GEEET!!!\n"

                        else:
                            self.request.send("ERROR: BAD COMMAND!\n")
                            self.request.close()
                            break
                    else:
                        self.request.send("ERROR: BAD COMMAND!\n")
                        self.request.close()
                        break
                else:
                    self.request.send("NEED AUTH!\n")
                    self.request.close()
                    break


            if reply is not None:
                self.request.send(reply)

    def hashcode(self):
        return base64.b64encode(str(time.time()))

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
