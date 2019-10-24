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
       
    def print(text):
        print(missatge)
        self.timeout=GLib.timeout_add(50, self.on_timeout, None)
        
    def main():
        #inicialitzar el client
		self.client = client()
		self.client.connect()
		self.client.thread_receive(self.print) #Quan usuari rebi del servidor la frase, es cridarà al mètode change que canviarà el label

if __name__ == "__main__":
	main()
