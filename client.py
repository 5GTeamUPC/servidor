import socket, select, string, sys, time, threading
from threading import Thread
from gi.repository import GLib

"""SYS:
This module provides access to some variables used or maintained by the interpreter and to functions that interact 
strongly with the interpreter. It is always available.
- sys.stdin(): is used for all interpreter input except for scripts but including calls to input() and raw_input()
- sys.stdout(): is used for the output of print and expression statements and for the prompts of input() and raw_input()

OBJECTIUS
- acabar el joc per consola
- juntar-ho!! (intentar-ho)
"""

class client():
    def connect(self):
        #self.nick = input("NICKNAME: ") #demanem nomes d'executar-se el client el nickname.

        # Creem el client_socket!
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 1234) # Adreça del servidor
        #Ens connectem al servidor, si es impossible connectar-se, surt directament.
        try:
            self.client_sock.connect((server_address))
        except:
            print("IMPOSSIBLE CONNECTAR-SE!")
            sys.exit()  #exit from python
        #self.client_sock.send(self.nick.encode('UTF-8'))
        print("Connexió establerta amb el servidor.")
        t1 = 0
        temps_total = 0


    def thread_receive(self, handler):
        thread = threading.Thread(target = self.receive, args = [handler])
        thread.daemon = True
        thread.start()
    def receive(self, handler):
        while 1:
            LLISTA_SOCKS = [sys.stdin, self.client_sock]

            # Select necessita que se li passin 3 llistes: The first is a list of the objects to be checked for incoming
            # data to be read, els altres 2 suda bastant la veritat.
            read_sockets, write_sockets, error_sockets = select.select(LLISTA_SOCKS, [], [])
            for sock in read_sockets:
                # Rebem missatges del servidor!
                if sock == self.client_sock:
                    data = sock.recv(4096)
                    if data:
                        self.t1 = time.time()
                        GLib.idle_add(handler, data)

    def send(self, missatge):
        
        temps_total = time.time() - self.t1
        self.client_sock.send(missatge)
