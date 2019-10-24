import gi
import Client2, time
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from Client2 import client



#Creem la nostra classe MainFinestra que heredarà de la superclasse Gtk.Window
class MainWindow(Gtk.Window):
	def __init__(self):

		#Cridem el constructor de la superclasse 
		Gtk.Window.__init__(self, title="EducaPlay")

		#Vector de finestres secundaries lligades a cada client
		#self.clientsGrafics= []
		#self.i=0

		self.set_default_size(800,400)

		#Colors de la finestra i els seus widgets
		self.cssProvider = Gtk.CssProvider();
		self.cssProvider.load_from_path('color.css')
		self.styleContext = Gtk.StyleContext()
		self.styleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
	
		#Label
		self.label = Gtk.Label()
		self.label2 = Gtk.Label()
		self.label3 = Gtk.Label()

		self.label.set_width_chars(80)
		self.label.set_label("BENVINGUTS AL JOC d'ordenar paraules!")
		self.label.set_size_request(800,250)
		self.label.set_name("labelBlue")
		
		self.label2.set_markup("\n<big><b>Instruccions:</b></big> Aquest joc consisteix en <b>organitzar</b> la frase desordenada que es mostri per pantalla amb el <b>menor temps</b> possible. El jugador que acabi més ràpid amb el mínim nombre d'errors, serà el guanyador. \n\n<big>                                         SORT!</big> ")
		self.label2.set_size_request(400,160)
		self.label2.set_name("tamany2")  
		#Trenca la frase i la recoloca si excedeix el tamany màxim del label
		self.label2.set_line_wrap(True)
		
		self.label3.set_markup("Insereixi el seu NOM per començar a jugar:")
		self.label3.set_size_request(100,170)
		self.label3.set_name("tamany")
		self.label3.set_line_wrap(True)

		#Entrada de text
		self.entry=Gtk.Entry()
		#Màxim nombre de caràcters que podem inserir
		self.entry.set_max_length(10)
		self.entry.set_name("entradaText")
		#Senyal que s'activa al polsar enter i cridarà a la funció usr_game
		name = self.entry.connect("activate", self.usr_game)

		#Grid (creem una grid ja que en la finestra principal no es pot inserir més d'un widget)
		self.grid=Gtk.Grid()
		self.add(self.grid)
		#columna, fila, amplada, altura
		self.grid.attach(self.label,0,0,5,1)
		self.grid.attach(self.label2,0,5,1,1)

		#ListBox
		self.box=Gtk.ListBox()
		self.grid.attach_next_to(self.box, self.label2, Gtk.PositionType.RIGHT,4,4)
		self.box.insert(self.label3, 0)
		self.box.insert(self.entry, 1)	


	def usr_game(self, widget):
		
		str_usuari=self.entry.get_text()
		self.entry.set_text("")
		window2=SecondWindow()
		# crear thread i despres fer lo d abaix al thread
		#thread.start(window(i).show_ll
		window2.label.set_markup("\nHola <big><b>" + str_usuari + "</b></big>!")
		#self.clientsGrafics(i)=window2
		#self.i=self.i + 1
		window2.connect("delete-event", Gtk.main_quit)
		window2.show_all()
		Gtk.main()


class SecondWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="EducaPlay")
		self.set_default_size(800,300)
		
		#frase_desordenada="fa esplèndit avui dia un"
		#Label
		self.label = Gtk.Label()
		self.label2 = Gtk.Label()
		self.label3 = Gtk.Label()
		#aligns per tal que el text es coloqui a la part superior esquerra
		self.label.set_name("labelBlue2")
		self.label.set_xalign(0.01)
		self.label.set_yalign(0)
		self.label.set_size_request(800,60)

		self.label2.set_markup("Esperi a que tots els usuaris es connectin...")
		self.label2.set_size_request(800,100)
		self.label2.set_name("tamany4")

		#self.label3.set_text(frase_desordenada)
		self.label3.set_size_request(800,120)
		self.label3.set_name("tamany3")
		#permet copiar i pegar del text
		self.label3.set_selectable(True)

		#Grid
		self.grid=Gtk.Grid()
		self.add(self.grid)
		self.grid.add(self.label)

		#Box
		self.box=Gtk.ListBox()
		self.grid.attach(self.box, 0, 5, 1, 1)
		self.box.insert(self.label2, 1)	
		self.box.insert(self.label3, 2)	
		
		
		#Entry
		self.entry=Gtk.Entry()
		self.entry.set_name("entradaText")
		self.entry.connect("activate", self.usr_frase)
		self.grid.attach(self.entry, 0, 10, 1, 1)

		
		#ProgressBar
		self.pb=Gtk.ProgressBar()
		#self.pb.set_fraction(0.6)
		self.grid.attach(self.pb, 0, 15, 1, 1)

		#inicialitzar el client
		self.client = client()
		self.client.connect()
		self.client.thread_receive(self.change) #Quan usuari rebi del servidor la frase, es cridarà al mètode change que canviarà el label

	
	def usr_frase(self, widget):
		frase_ordenada=self.entry.get_text()
		self.temps=time.time()-self.start_time
		self.client.send((frase_ordenada+"-t"+str(self.temps)).encode('UTF-8'))
		self.entry.set_text("")
		self.pb.destroy()
		self.client.thread_receive(self.change2)
		self.label2.set_markup("Esperant resultats... KEEP CALM!")

	def on_timeout(self, data):
		nou_valor=self.pb.get_fraction()+0.001
		self.pb.set_fraction(nou_valor)
		return True

	def change(self, frase_desordenada):
		self.start_time=time.time()  
		self.label2.set_markup("Ordeni la següent frase: ")
		self.label3.set_text(frase_desordenada.decode('UTF-8'))
		self.timeout=GLib.timeout_add(50, self.on_timeout, None)

	def change2(self, resultats):
		self.label2.set_markup("<b>RESULTAT:</b>")
		self.label2.set_name("boto")
		self.label3.set_name("tamany5")
		self.label3.set_markup(resultats)

		
		

if __name__=="__main__":
	window = MainWindow()  
	#S'atura el programa quan polsem la creu
	window.connect("delete-event", Gtk.main_quit)
	#Mostem la finestra
	window.show_all()
	Gtk.main()


