import socket, select, threading, random, time

"""SELECT: 
Python’s select() function is a direct interface to the underlying operating system implementation. It monitors sockets,
open files, and pipes (anything with a fileno() method that returns a valid file descriptor) until they become readable 
or writable, or a communication error occurs. select() makes it easier to monitor multiple connections at the same time,
and is more efficient than writing a polling loop in Python using socket timeouts, because the monitoring happens in the
operating system network layer, instead of the interpreter.

The arguments to select() are three lists containing communication channels to monitor. The first is a list of the 
objects to be checked for incoming data to be read, the second contains objects that will receive outgoing data when 
there is room in their buffer, and the third those that may have an error (usually a combination of the input and output
channel objects). 
"""
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
#        num = 0
        n_sim = 0
#        read_sockets = []
#        write_sockets = []
#        error_sockets = []
#        num_jugadors = 0 #Pel while de rebre la data!
#        temps = []
#        jugador_nick = []
#        numeroerrors = []
#        fraseclient = []
#        errors = []
#        line = open("BaseDades.txt").read().splitlines()
#        frase = random.choice(line)

        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creem el server_socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #Això no sé que fa però mai va de menys
        self.server_socket.bind(("localhost", 1234))   # bind() --> per associar un socket a la direcció d'un servidor. host: IP port: 1234
        self.server_socket.listen(10)  # Ens posem en mode escoltar (escoltem les connexions entrants dels clients!)
        #print("[#] Servidor creat!")
        #afegim a la llista de sockets el server_socket
        self.LLISTA_SOCKS.append(self.server_socket)
        #print("[#] Servidor afegit a la llista de sockets!!")
        #print(self.LLISTA_SOCKS)
        while 1:
            # Select necessita que se li passin 3 llistes: The first is a list of the objects to be checked for incoming
            # data to be read, els altres 2 suda bastant la veritat.
            read_sockets, write_sockets, error_sockets = select.select(self.LLISTA_SOCKS, [], [])

            num = num +1
            # Miren dels read_sockets aver si algu demana o diu algo!
            for sock in read_sockets:
                # Nova connexió!
                if(sock == self.server_socket and joc == False):
                    # Quan rebem data del servidor, significa que una nova connexió s'ha rebut des del server_socket
                    client_sock, client_addr = self.server_socket.accept() #Acceptem la connexió
                    self.LLISTA_SOCKS.append(client_sock) #Afegim el clint a la llista!
                    #mapa.setdefault(nick, client_sock)
                    n_sim = n_sim + 1 #incrementem el número de jugadors!
                    #print(nick)
                    #self.missatge_broadcast("Nou jugador: %s" % nick)

                if(len(self.LLISTA_SOCKS) == 4 and joc == False):   #Si el número de jugadors és 3 comencem el joc!
                    time.sleep(1)
                    self.send_frase(self.vector_frase)
                    joc = True
                else:
                    message = self.receive_message(sock)
                    if(message != False):
                        missatge_nick = message.split("-t")
                        vector = missatge_nick[0].split(" ")
                        cont = 0
                        errors = 0
                        if (len(vector) == len(self.frase_vector)):
                            for i in vector:
                                if self.frase_vector[cont].lower() != i.lower():
                                    errors = errors + 1
                                cont = cont + 1
                        else:
                            errors = len(vector)
                        print(errors)
                        print(int(float(missatge_nick[1])))
                        suma = errors + int(float(missatge_nick[1]))
                        self.send_message(sock,"HAS GUANYAT! ETS EL MÉS RÀPID CULEGA!")
                        self.LLISTA_SOCKS_RETORN[self.pppp] = sock
                        #incrementem la posició del vector
                        if(self.pppp == 2):
                            #self.ordre_guanyador = self.ordre(self.ordre_guanyador)
                            self.send_message(self.LLISTA_SOCKS_RETORN[0],"HAS GUANYAT! ETS EL MÉS RÀPID CULEGA!")
                            self.send_message(self.LLISTA_SOCKS_RETORN[1],"HAS PERDUT... PERÒ HAS QUEDAT SEGON JEJ")
                            self.send_message(self.LLISTA_SOCKS_RETORN[2],"HAS PERDUT")
                            #self.ordre_guanyador.index(max(self.ordre_guanyador))
                        self.pppp = self.pppp + 1
if __name__ == "__main__":
    s = server()
    s.run()
