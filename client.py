import socket, select, string, sys, time, threading
from threading import Thread

class client():
    def connect(self):
        IP = 'localhost'
        port = 1234
        # Creem el client_socket
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (IP, port) # Adreça del servidor
        #Ens connectem al servidor, si es impossible connectar-se, surt directament.
        try:
            self.client_sock.connect((server_address))
        except:
            print("Impossible connectar-se!")
            sys.exit()  #exit from python
        print("Connexió establerta amb el servidor.")

    def thread_receive(self, handler):
        thread = threading.Thread(target = self.receive, args = [handler])
        thread.daemon = True
        thread.start()
        
    def receive(self):
        while 1:
            LLISTA_SOCKS = [sys.stdin, self.client_sock]
            # Select necessita que se li passin 3 llistes: The first is a list of the objects to be checked for incoming
            # data to be read, els altres 2 suda bastant la veritat.
            read_sockets, write_sockets, error_sockets = select.select(LLISTA_SOCKS, [], [])
            for sock in read_sockets:
                # Rebem missatges del servidor!
                if sock == self.client_sock:
                    data = sock.recv(4096)
#                    print(data)

    def receive_message(self, socket_client):
        try:
            message = socket_client.recv(1024)
            if not len(message):
                return False
            return message.decode('UTF-8')
        except:
            return False

    def send_message(self, missatge):
        self.client_sock.send(missatge.encode('UTF-8'))
       

    def run(self):
        read_sockets = []
        write_sockets = []
        error_sockets = []
        while 1:
            self.LLISTA_SOCKS = [sys.stdin, self.client_sock]
            read_sockets, write_sockets, error_sockets = select.select(self.LLISTA_SOCKS, [], [])
            for sock in read_sockets:
            # Rebem missatges del servidor!
                if sock == self.client_sock:
                    data = self.receive_message(sock)
                if not data:
                    data = 0
                    #sys.exit()
#                else:
#                    print("\n%s" % data)
#                    print data
#                    sys.stdout.write(data)
#                    prompt()

            # Quan el client vol enviar un missatge
            else:
                message = sys.stdin.readline()
                self.send_message(message)
                print("Missatge enviat!!")
        
if __name__ == "__main__":
	c = client()
	c.connect()
	c.run()
