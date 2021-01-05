#Importar librerias
import json
import requests
import screen
import pymongo


#Variables para el Token y la URL del chatbot
TOKEN = "" 
URL = "https://api.telegram.org/bot" + TOKEN + "/"
 
 
# conexiÃ³n a Mongo
def conexion():
	client = pymongo.MongoClient('127.0.0.1',27017)
	client.server_info()  
	return client 
	
#almacenar los datos a mongodb
def almacena(nombre,texto):
	client = conexion()
	data = {}
	data['Nombre'] = nombre
	data['Mensaje'] = texto
	try:
		destination = 'chat'
		database = 'ChatBot'
		collection = client[database][destination]
		collection.insert_one(data)
	except Exception as error:
		print("Error guardando los datos: %s" % str(error))
	client.close()
 
def update(offset):
	#Llamar al metodo getUpdates del bot, utilizando un offset
	respuesta = requests.get(URL + "getUpdates" + "?offset=" + str(offset) + "&timeout=" + str(100))
	 
	 
	#Decodificar la respuesta recibida a formato UTF8
	mensajes_js = respuesta.content.decode("utf8")
	 
	#Convertir el string de JSON a un diccionario de Python
	mensajes_diccionario = json.loads(mensajes_js)
	 
	#Devolver este diccionario
	return mensajes_diccionario
 
def info_mensaje(mensaje):
 
	#Comprobar el tipo de mensaje
	if "text" in mensaje["message"]:
		tipo = "texto"
	elif "sticker" in mensaje["message"]:
		tipo = "sticker"
	elif "animation" in mensaje["message"]:
		tipo = "animacion" 
	elif "photo" in mensaje["message"]:
		tipo = "foto"
	else:
		tipo = "otro"
 
	#Recoger la info del mensaje (remitente, id del chat e id del mensaje)
	persona = mensaje["message"]["from"]["first_name"]
	id_chat = mensaje["message"]["chat"]["id"]
	id_update = mensaje["update_id"]
 
	#Devolver toda la informacion
	return tipo, id_chat, persona, id_update
 
def leer_mensaje(mensaje):
 
	#Extraer el texto, nombre de la persona e id del Ãºltimo mensaje recibido
	texto = mensaje["message"]["text"]
 
	#Devolver las dos id, el nombre y el texto del mensaje
	return texto
 
def enviar_mensaje(idchat, texto):
	#Llamar el metodo sendMessage del bot, passando el texto y la id del chat
	requests.get(URL + "sendMessage?text=" + texto + "&chat_id=" + str(idchat))
 
 
 
#Variable para almacenar la ID del ultimo mensaje procesado
ultima_id = 0
 
while(True):
	mensajes_diccionario = update(ultima_id)
	for i in mensajes_diccionario["result"]:
 
		#Guardar la informacion del mensaje
		tipo, idchat, nombre, id_update = info_mensaje(i)
 
		#Generar una respuesta dependiendo del tipo de mensaje
		if tipo == "texto":
			texto = leer_mensaje(i)
			texto = texto.lower()
			
			if "/start" in texto or "hola" in texto.lower():
				texto_respuesta = "Hola soy el bot asistente para caja negra,  en que te puedo ayudar. \nPuedes consultar: \n\n* Servidores - Tipos de servidores que manejamos.\n* Hosting - Planes de hosting con los que contamos. \n* Contratar - Contratar algÃºn servicio. \n\nPara elegir una de las opciones anteriores por favor envia la palabra relacionada con el servicio que desea consultar."

			elif "gracias" in texto:
				texto_respuesta = "Estamos para servirte :D!"

			elif "adios" in texto or "adiÃ³s" in texto:
				texto_respuesta = "Hasta pronto :D!"

			elif "contratar" in texto or "contrataciÃ³n" in texto or "contratacion" in texto:
				almacena(nombre,texto)
				texto_respuesta = "Puedes ingresar los datos con la palabra contrato seguido de tu nombre, nÃºmero de telefono, correo y el servicio a contratar, en caso de ser un servicio presencial especifique la direcciÃ³n. \nEjemplo: \nContrato Alexa Luna Lira 4270000000 ejemplo_1@gmail.com servidor gps av.de los patos nÃ¹mero 2"

			elif "contrato" in texto:
				#"enviar_mensaje(1387340486, texto)"
				almacena(nombre,texto)
				texto_respuesta = "Tus datos fueron enviados a uno de nuestros asesores, en un momento nos contactaremos contigo, fue un placer servirle :D"


			elif "linux" in texto:
				almacena(nombre,texto)
				texto_respuesta = "La informaciÃ³n la puede encontrar en el siguiente link: https://caja-negra.com.mx/planes-vps-gl/"

			elif "windows" in texto:
				almacena(nombre,texto)
				texto_respuesta = "La informaciÃ³n la puede encontrar en el siguiente link: https://caja-negra.com.mx/planes-vps-ws/"


			elif "servidor" in texto or "servidores" in texto:
				almacena(nombre,texto)
				texto_respuesta = "Contamos con servidores virtuales privados windows o linux, elija una de las siguientes opciones \n* Windows \n*Linux"

			elif "estudiantes" in texto or "estudiante" in texto:
				almacena(nombre,texto)
				texto_respuesta = "OK, los planes para estudiantes los puede consultar en el siguiente link: https://caja-negra.com.mx/planes-hosting-estudiante/  si desea contratar un plan, porfavor ingrese sus datos"

			elif "empresarial" in texto or "empresa" in texto or "empresas" in texto:
				almacena(nombre,texto)
				texto_respuesta = "El costo esta en el siguiente link: https://caja-negra.com.mx/planes-hosting/"


			elif "hosting" in texto:
				almacena(nombre,texto)
				texto_respuesta = "Contamos con diversos planes de hosting, elige la opcion que mas te convenga: \n* Estudiantes \n* Empresarial"


			else:
				almacena(nombre,texto)
				texto_respuesta = "no encuentro respuesta a tu pregunta lo siento :("
				
		#Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
		if id_update > (ultima_id-1):
			ultima_id = id_update + 1
 
		#Enviar la respuesta
		enviar_mensaje(idchat, texto_respuesta)
 
	#Vaciar el diccionario
	mensajes_diccionario = [] 
