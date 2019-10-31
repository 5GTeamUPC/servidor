import socket, select, threading, random, time

class server:
    def __init__(self):
        self.errors = []
        self.times = []
        self.ordre_correcte = []
        self.LLISTA_SOCKS = []   #Llista amb el conjunt de tots els sockets (servidor i clients)
        self.LLISTA_SOCKS_RETORN = []
        self.ordre_guanyador = []
        self.pppp = 0

    def receive_message(self, socket_client):
        try:
            message = socket_client.recv(1024)
            if not len(message):
                return False
            return message.decode('UTF-8')
        except:
            return False

    def send_message(self, sock, message):
        sock.send(message.encode('UTF-8'))

    def missatge_broadcast (self, message):
        for socket in self.LLISTA_SOCKS:
            if socket != self.server_socket: #No hem d'enviar el missatge al server_socket!!
                try:
                    socket.send(message.encode('UTF-8'))
                except: #Que hi ha hagi una excepció significa que algo no va del tot bé
                    socket.close()
                    self.LLISTA_SOCKS.remove(socket)

    def run(self):
        mapa = {}  #Mapa amb tots els host i clients
        n_sim = 0
        read_sockets = []
        write_sockets = []
        error_sockets = []
#        line = open("BaseDades.txt").read().splitlines()
#        frase = random.choice(line)

        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creem el server_socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #Això no sé que fa però mai va de menys
        self.server_socket.bind(("localhost", 1234))   # bind() --> per associar un socket a la direcció d'un servidor. host: IP port: 1234
        self.server_socket.listen(10)  # Ens posem en mode escoltar (escoltem les connexions entrants dels clients!)
        #print("[#] Servidor creat!")
        self.LLISTA_SOCKS.append(self.server_socket) #afegim a la llista de sockets el server_socket
        #print("[#] Servidor afegit a la llista de sockets!!")
        #print(self.LLISTA_SOCKS)
        while 1:
            # Select necessita que se li passin 3 llistes: The first is a list of the objects to be checked for incoming
            # data to be read, els altres 2 suda bastant la veritat.
            read_sockets, write_sockets, error_sockets = select.select(self.LLISTA_SOCKS, [], [])

            for sock in read_sockets: #Miren dels read_sockets aver si algu demana o diu algo!
                #Nova connexió!
                if(sock == self.server_socket):
                    # Quan rebem data del servidor, significa que una nova connexió s'ha rebut des del server_socket
                    client_sock, client_addr = self.server_socket.accept() #Acceptem la connexió
                    self.LLISTA_SOCKS.append(client_sock) #Afegim el client a la llista!
                    n_sim = n_sim + 1 #incrementem el número de jugadors!
                    println(self.LLISTA_SOCKS)
                    self.missatge_broadcast("nou usuari connectat")
                #Algun sim7000 vol dir alguna cosa
                else:
                    message = self.receive_message(sock)
                    print(message)
                    if(message != False):
                        self.missatge_broadcast(message)
                    if(message = False):
                        self.LLISTA_SOCKS.remove(sock)
                        println(self.LLISTA_SOCKS)
                        println("Socket desconnectat")
if __name__ == "__main__":
    s = server()
    s.run()
