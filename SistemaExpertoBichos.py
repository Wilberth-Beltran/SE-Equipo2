import tkinter as tk
from tkinter import ttk
import tkinter as tkkk
from tkinter import filedialog
import sqlConnector as sqlbd
import cv2 as ocv
import os 

preguntas = ["¿Qué tamaño tiene?",
			 "¿Cuántas patas tiene el bicho?",
			 "¿Color del bicho?",
			 "¿Cómo se desplaza?"]

preguntase = ["Tamaño del bicho: ", 
             "cuantas patas vez: ", 
             "Color del bicho: ", 
             "Como se desplaza: "]

base_temp = sqlbd.BaseDatos(**sqlbd.acceso_bd)

opciones = [base_temp.gettamaño(), 
			base_temp.getpatas(), 
			base_temp.getColor(), 
			base_temp.getdesplazamiento()]

respuestas = {}
preguntas2 = []
dialogo = None

class ventanaExperto:
	archivo = None
	vActual = None
	ventanaa = None

	#Arbol de verificacion################################################################################
	Tamaños = base_temp.gettamaño()
	patas = base_temp.getpatas()
	colores = base_temp.getColor()
	desplazamientos = base_temp.getdesplazamiento()
	combinaciones = []
	bichos = base_temp.getbichos()
	i = 0
	for Tamaño in Tamaños:
		for pata in patas:
			for color in colores:
				for desplazamiento in desplazamientos:
					#print(tamaño, color, patas, desplazamiento)
					combinaciones.append([Tamaño, pata, color, desplazamiento, 0])
					i+=1

	print(i)
	x=0
	for num in range(6):
		print(num)
		x+=1

	j=0
	for bichitos in bichos:
		for combinacion in combinaciones:
			if((bichitos[1] == combinacion[0]) & (bichitos[2] == combinacion[1]) & (bichitos[3] == combinacion[2]) & (bichitos[4] == combinacion[3])):
				combinacion[4]+=1
				#print(combinacion)
				j+=1
	print(j)
	print("Combinaciones ocupadas: ")
	for combinacion in combinaciones:
		if (combinacion[4]>0):
			print (combinacion)

	k=0
	print("Combinaciones faltantes: ")
	for combinacion in combinaciones:
		if (combinacion[4]==0):
			print (combinacion)
			k+=1
			if(k==34):
				print("Separador: \n")
			if(k==68):
				print("Separador: \n")
			if(k==102):
				print("Separador: \n")
			
	print(k)

	#Arbol de verificacion##################################

	def getOpciones(self):
		self.opciones = [base_temp.gettamaño(), 
			base_temp.getpatas(), 
			base_temp.getColor(), 
			base_temp.getdesplazamiento()]

	def __init__(self):

		bienvenida = tk.Tk()
		#Titulo principal
		bienvenida.title("SISTEMA EXPERTO DEL BICHO QUE OBSERVASTE")
		#bienvenida.geometry("960x600")
		bienvenida.resizable(width=False, height=False)

		wtotal = bienvenida.winfo_screenwidth()
		htotal = bienvenida.winfo_screenheight()

		wventana = 960
		hventana = 600

		pwidth = round(wtotal/2-wventana/2)
		pheight = round(htotal/2-hventana/2)

		bienvenida.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

		bg = tk.PhotoImage(file="Imagenes/Fondo.png")
		bg_lbl = tk.Label(bienvenida, image=bg).place(x=-2, y=0)

		ASD = base_temp.consulta("SELECT * FROM bichos")

		label_text =tk.Label(bienvenida, background="#000000", text="Bienvenido al Sistema Experto Clasificador de BICHOS \n"
							"aqui podras buscar entre todas las especies del \n"
							"Mundo con un total de "+ASD.fetchall().__len__().__str__()+" especies, actualmente registradas.", font=("Arial",16), foreground="white")
		
		label_text.pack(side=tk.TOP, pady=20)
		frame_boton = tk.Frame(bienvenida, background="#c27f44")
		boton_seguir = tk.Button(frame_boton, text="Iniciar", command=lambda: self.mostrar_ventana_usuario(), font=("Arial",14), border=0, bg="white")
		frame_boton.pack(side=tk.TOP)
		boton_seguir.pack()
		
		self.vActual = bienvenida
		self.vActual.update()
		self.vActual.mainloop()

	def dialogo(self, titulo, texto, **kwargs):
		dialogo = tk.Tk()
		dialogo.title(titulo)
		dialogo.configure(background="white")
		label_text =tk.Label(dialogo, pady=10, padx=10,background="white" ,text=texto)
		#label_text.pack()
		frame_boton = tk.Frame(dialogo, background="white",padx=10,pady=10)
		boton_aceptar = tk.Button(frame_boton, text="Aceptar", command=dialogo.destroy, pady=10, padx=10)
		label_text.pack()
		frame_boton.pack()
		boton_aceptar.pack()

	def nueva_opcion(self):
		ventana = tk.Tk()
		ventana.title("Nueva Opcion")
		ventana.configure(background="white")
		lbl_o = tk.Label(ventana, background="white", text="Opcion: ", font=("arial", 16))
		combo_o = ttk.Combobox(ventana, values=["Patas", "Desplazamiento", "Color", "Tamaño"], state="readonly", background="white", font=("arial",16))
		lbl_no = tk.Label(ventana, background="white", text="Nueva opcion: ", font=("arial", 16))
		ent_no = tk.Entry(ventana, font=("arial",16), background="white")
		lbl_o.grid(row=0, column=0, padx=10, pady=5)
		combo_o.grid(row=1, column=0, padx=10, pady=5)
		lbl_no.grid(row=0, column=1, padx=10, pady=5)
		ent_no.grid(row=1, column=1, padx=10, pady=5)

		frame_buttons = tk.Frame(ventana, background="white")
		frame_buttons.grid(row=2,column=0, columnspan=2, pady=10)

		ingresar_button = tk.Button(frame_buttons, text="Ingresar", command=lambda: self.insertarCategoria(combo_o.get(), ent_no.get()), font=("arial",16))
		ingresar_button.grid(row=0, column=0, pady=10, padx=5)

		imagen_button = tk.Button(frame_buttons, text="Salir", command=lambda: self.salirCategoria(ventana), font=("arial",16))
		imagen_button.grid(row=0, column=1, pady=10, padx=5)
		

	def insertarCategoria(self, categoria, no):
		if (categoria=="Tamaño"):
			base_temp.insertarTamaño(no)
			self.dialogo("Message", "Se ha ingresado la opcion correctamente")
		elif (categoria=="Patas"):
			base_temp.insertarColor(no)
			self.dialogo("Message", "Se ha ingresado la opcion correctamente")
		elif (categoria=="Color"):
			base_temp.insertarCuerpo(no)
			self.dialogo("Message", "Se ha ingresado la opcion correctamente")
		elif (categoria=="Desplazamiento"):
			base_temp.insertarDesplazamiento(no)
			self.dialogo("Message", "Se ha ingresado la opcion correctamente")
		else: 
			print("No se encontro la categoria")
		
	def salirCategoria(self, V2):
		V2.destroy()
		self.mostrar_ventana_experto(False)


	def sin_coincidencias(self):
		self.ventanaa = tk.Tk()
		self.ventanaa.title("Sin Coincidencias")
		self.ventanaa.configure(background="white")

		label_text =tk.Label(self.ventanaa, pady=10, padx=10,background="white" ,text="No se encontraron coincidencias, desea agregar la nueva seleccion?")
		label_text.pack()
		frame_boton = tk.Frame(self.ventanaa, background="white",padx=10,pady=10)
		boton_aceptar = tk.Button(frame_boton, text="Si", command=lambda: self.mostrar_ventana_experto(True), pady=10, padx=10)
		boton_cancelar = tk.Button(frame_boton, text="No", command=self.ventanaa.destroy, pady=10, padx=10)
		boton_aceptar.grid(row=0, column=0, pady=10, padx=10)
		boton_cancelar.grid(row=0, column=1, pady=10, padx=10)
		frame_boton.pack()

	def meterbicho(self, Nombre, dropdowns, Descripcion):

		if((Nombre.strip(' ').__len__()==0) | (dropdowns.__len__() < 4) | (Descripcion.strip(' ').__len__()==0) | (self.archivo==None)):
			self.dialogo("Error", "Tienes alguna respuesta vacia, porfavor llene todos los campos")
			return
		r = []
		for item in dropdowns:
			r.append(item.get())

		based = sqlbd.BaseDatos(**sqlbd.acceso_bd)

		s = based.buscarnombre(Nombre)

		if(s):
			self.dialogo("Error", "La especie ya existe, intente nuevamente")
			return

		try:
			based.meterbicho(Nombre,r[0], r[1], r[2], r[3], Descripcion)
			imagen = ocv.imread(self.archivo, ocv.IMREAD_COLOR)
			ocv.imwrite('Imagenes/'+Nombre+'.png',imagen)
			#buscara la imagen y agregara el nombre con la extencion
			self.dialogo("Message", "Se ha ingresado el bicho correctamente")
		except:
			self.dialogo("Error", "Ocurrion un error, intente nuevamente")
		
	def abrir_imagen(self, *args):
		self.archivo=filedialog.askopenfilename(
					 initialdir="/", 
				     title="Selecciona la imagen", 
					 filetypes=(("png files","*.png"), ("all files","*.*")))
		imagen = ocv.imread(self.archivo, ocv.IMREAD_COLOR)
		resized = ocv.resize(imagen, (300,300), interpolation=ocv.INTER_AREA)
		ocv.imwrite('img_temp.png',resized)
		self.archivo = 'img_temp.png'
		img =tk.PhotoImage(file=self.archivo)
		lbl_img = tk.Label(self.vActual, image=img)
		lbl_img.grid(row=2, column=2, rowspan=8,padx=10)

		self.vActual.update()
		self.vActual.mainloop()

	def setRespuesta(self, respuesta, *args):
		print(respuesta)

	def rm(path):
		if os.path.isdir(path):  
			print("Imposible borrar {0}!. Es una carpeta.".format(path))  
		elif os.path.isfile(path):  
			try:
				os.remove(path)
			except OSError as e:
				print ("Error: %s - %s." % (e.filename,e.strerror))
		else:  
			print("Error. No se ha encontrado {0}.".format(path)) 

	def mostrar_ventana_experto(self, boolean):
		self.vActual.destroy()
		self.getOpciones()
		if(boolean):
			self.ventanaa.destroy()

		dropdowns = []
		ventana = tk.Tk()
		ventana.title("Clasificator de Bichos")
		ventana.configure(background="white")

		wtotal = ventana.winfo_screenwidth()
		htotal = ventana.winfo_screenheight()

		wventana = 900
		hventana = 685

		pwidth = round(wtotal/2-wventana/2)
		pheight = round(htotal/2-hventana/2)

		ventana.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

		bg = tk.PhotoImage(file="Imagenes/Fondo.png")
		bg_lbl = tk.Label(ventana, image=bg).place(x=-2, y=0)

		label_titulo = tk.Label(ventana, text="Seleccione las caracteristicas de la Serpiente a Ingresar", font=("arial",20), background="#51524a", foreground="white")
		label_titulo.grid(row=0, column=0, pady=20, padx=10, columnspan=3)

		nombre = tk.Label(ventana, text="Nombre: ", font=("arial",16), background="#265046", foreground="white")
		nombre.grid(row=1, column=0, sticky=tk.W, padx=20)

		nombreE = tk.Entry(ventana, font=("arial",16), background="white")
		nombreE.grid(row=1,column=1)

		for i, pregunta in enumerate(preguntase):

			pregunta = tk.Label(ventana, text=pregunta, font=("arial",16), background="#265046", foreground="white")
			pregunta.grid(row=i+2, column=0, sticky=tk.W, padx=15, pady=0)

			opcionesA = self.opciones[i]
			respuesta_dropdown = ttk.Combobox(ventana, values=opcionesA, state="readonly", background="white", font=("arial",16))
			dropdowns.append(respuesta_dropdown)
			respuesta_dropdown.grid(row=i+2, column=1, padx=20)

		explicacion_lbl = tk.Label(ventana, text="Explicacion: ", font=("arial",16), background="#265046", foreground="white")
		explicacion_lbl.grid(row=10, column=0, sticky=tk.N+tk.W+tk.S, padx=20, pady=15,rowspan=2)

		explicacion_e = tk.Text(ventana, font=("arial",16), background="white", height=3, width=50)
		explicacion_e.grid(row=10,column=1, padx=10, pady=15, rowspan=1, columnspan=2)

		frame_buttons = tk.Frame(ventana, background="#265046")
		frame_buttons.grid(row=12,column=0, columnspan=5, pady=00)

		ingresar_button = tk.Button(frame_buttons, text="Ingresar", command=lambda: self.meterbicho(nombreE.get(), dropdowns, explicacion_e.get("1.0", "end-1c")), font=("arial",16), border=0)
		ingresar_button.grid(row=0, column=0, pady=10, padx=5)

		imagen_button = tk.Button(frame_buttons, text="Imagen", command=self.abrir_imagen, font=("arial",16), border=0)
		imagen_button.grid(row=0, column=1, padx=5)

		volver_button = tk.Button(frame_buttons, text="Volver", command=self.mostrar_ventana_usuario, font=("arial",16), border=0)
		volver_button.grid(row=0, column=2, padx=5)

		agcat_button = tk.Button(frame_buttons, text="Agregar Opcion", command=self.nueva_opcion, font=("arial",16), border=0)
		agcat_button.grid(row=0, column=3, padx=5)

		label_img = tk.Label(ventana, text="Imagen:", font=("arial",18), background="black", foreground="white")
		label_img.grid(row=1, column=2, pady=12, padx=10)

		#img =tk.PhotoImage(file="Imagenes/Background3.png")
		#lbl_img = tk.Label(ventana, image=img)
		#lbl_img.grid(row=2, column=2, rowspan=4, padx=13, pady=25)

		self.vActual = ventana

		self.vActual.mainloop()

	def mostrar_respuestas(self, dropdowns, **kwargs):
		base_datos = sqlbd.BaseDatos(**sqlbd.acceso_bd)
		r = []
		for item in dropdowns:
			r.append(item.get())

		for item in r:
			if(item.strip(' ').__len__()==0):
				self.dialogo("Error", "Tienes alguna opcion vacia, porfavor llene todos los campos")
				return
		consulta = base_datos.buscarbicho(r[0], r[1], r[2], r[3])
		for bichitos in consulta:
			print (bichitos)
		consulta = base_datos.buscarbicho(r[0], r[1], r[2], r[3])
		if(consulta.fetchall().__len__()>0):
			consulta2 = base_datos.buscarbicho(r[0], r[1], r[2], r[3])

			self.vActual.destroy()
			ventana = tkkk.Tk()
			ventana.title("Respuestas")
			ventana.configure(background="white")

			#bg = tk.PhotoImage(file="Imagenes/Background6.png")
			#bg_lbl = tk.Label(ventana, image=bg).place(x=-2, y=0)

			i = 0
			frames = []
			#img23 = None
			for Nombre, Descripcion in consulta2:
				if(i<2):
					#print(nombre, explicacion)
					frame = tkkk.Frame(ventana, background="white")
					frame.grid(row=i, column=0, pady=10)
					
					lbl_especie = tkkk.Label(frame, text="Especie: ", font=("arial",16), background="white")
					lbl_especie.grid(row=0, column=0, padx=20)

					lbl_especie = tkkk.Label(frame, text=Nombre, font=("arial",16), background="white")
					lbl_especie.grid(row=1, column=0, padx=20, pady=10)

					img23 = tk.PhotoImage(file="Imagenes/"+Nombre+".png")

					lbl_img = tkkk.Label(frame, image=img23)
					lbl_img.image = img23
					lbl_img.grid(row=2, column=0, padx=10)

					#print("Imagenes/"+nombre+".png")
					frame.Descripcion = Descripcion
					frames.append(frame)

				i+=1

			btn_explicacion = tkkk.Button(frame, text="Descripcion", command=lambda: self.ver_explicacion(frames), font=("arial",16))
			btn_explicacion.grid(row=i*3, column=0, columnspan=3, padx=20, pady=20)

			btn_salir = tkkk.Button(ventana, text="Volver", command= lambda: self.mostrar_ventana_usuario(), font=("arial",16))
			btn_salir.grid(row=i*3+1, column=0, columnspan=3, padx=20, pady=20)

			self.vActual = ventana
			self.vActual.update()
			self.vActual.mainloop()
		else:
			print("No se encontraron coincidencias")
			self.sin_coincidencias()
			
	def ver_explicacion(self, frames):
		for frame in frames:
				lbl_explicacion = tk.Label(frame, text="Descripcion: ", font=("arial",16), background="white")
				lbl_explicacion.grid(row=0, column=3)

				lbl_explicacion = tk.Label(frame, text=frame.Descripcion, font=("arial",11), background="white") #aquiii
				lbl_explicacion.grid(row=1, column=3, rowspan=3)

	def cerrar_ventana(ventana):
		ventana.destroy()

	def mostrar_ventana_usuario(self):
		self.getOpciones()
		self.vActual.destroy()

		dropdowns = []

		ventana = tk.Tk()
		ventana.title("Bichos")
		ventana.resizable(width=False, height=False)
		ventana.configure(background="white")

		wtotal = ventana.winfo_screenwidth()
		htotal = ventana.winfo_screenheight()

		wventana = 770
		hventana = 540

		pwidth = round(wtotal/2-wventana/2)
		pheight = round(htotal/2-hventana/2)

		ventana.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

		bg = tk.PhotoImage(file="Imagenes/Background4.png")
		bg_lbl = tk.Label(ventana, image=bg).place(x=-2, y=0)

		label_titulo = tk.Label(ventana, text="Seleccione las caracteristicas del Bicho", font=("Open Sans",20), background="#51524a", foreground="white")
		label_titulo.grid(row=0, column=0, pady=20, columnspan=5)

		for i, pregunta in enumerate(preguntas):

			pregunta = tk.Label(ventana, text=pregunta, font=("Open Sans",16), background="#c1ff72")
			pregunta.grid(row=i+1, column=0, sticky=tk.W, padx=17, pady=15)

			opcionesA = self.opciones[i]
			respuesta_dropdown = ttk.Combobox(ventana, values=opcionesA, state="readonly", background="#58a292", font=("arial",16))
			dropdowns.append(respuesta_dropdown)
			respuesta_dropdown.grid(row=i+1, column=1, padx=24, )

		frame_buttons = tk.Frame(ventana, background="white")
		frame_buttons.grid(row=12,column=0, columnspan=3, pady=30)

		ingresar_button = tk.Button(frame_buttons, text="Mostrar respuestas", command=lambda: self.mostrar_respuestas(dropdowns), font=("arial",16), border=0)
		ingresar_button.grid(row=0, column=0)

		self.vActual = ventana
		self.vActual.mainloop()

asd = ventanaExperto()
