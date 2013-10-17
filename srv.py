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
            reply  = None
            data   = None
            parsed = None 
            try:
                data   = self.request.recv(1024)
                data   = data.replace('\r', '')
                data   = data.replace('\n', '')
                parsed = self.parse_data(data, code)
            except:
                pass

            if data == "HELO" or data == "EHLO":
                reply = "HELO " + code + "\n"

            elif "PING" in data:
                if parsed != "ERROR":
                    reply = "PONG " + code + "\n"
                else:
                    self.request.send("ERROR: BAD PING!\n")
                    self.request.close()
                    break

            elif "QUIT" in data or "EXIT" in data:
                self.request.send("BYE BYE!\n")
                self.request.close()
                break
            
            elif "USER" in data:
                if parsed != "ERROR":
                    user = parsed[2]
                else:
                    self.request.send("ERROR: BAD PING!\n")
                    self.request.close()
                    break

            elif "PASS" in data:
                if parsed != "ERROR":
                    #DB validate user:pass
                    passw = parsed[2]
                    reply = "OK " + code + " " + user + "\n"
                    login = True
                else:
                    self.request.send("ERROR: BAD PING!\n")
                    self.request.close()
                    break

            elif "GET" in data:
                if login == True:
                    if parsed != "ERROR":
                        #Process command from GET
                        reply = "GEEET!!!\n"
                    else:
                        self.request.send("ERROR: BAD PING!\n")
                        self.request.close()
                        break
                else:
                    self.request.send("ERROR: NEED AUTH!\n")
                    self.request.close()
                    break
           
            if reply is not None:
                self.request.send(reply)

    def hashcode(self):
        return base64.b64encode(str(time.time()))

    def parse_data(self, cadena, traza):
        if " " in cadena:
            coderecv = cadena.split(" ")

            if coderecv[1] == traza:
                return coderecv
            else:
                return "ERROR"
        else:
            return "ERROR"

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
