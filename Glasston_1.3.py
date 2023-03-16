#----------------- Importacion de Librerias --------------------#
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.by import By
import re
from unicodedata import normalize
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pyModbusTCP.client import ModbusClient
import snap7
import time
from datetime import datetime
import snap7.client as c
from snap7.util import *
from snap7.types import *
#from snap7.snap7types import *
import ctypes
from ctypes import *
from enum import Enum
from snap7.common import ADict
from time import sleep
from pylogix import PLC
import math
from MensajesTXT import MensajesAlarmas
from OsmosisP2 import Osmosis
from HornoGlasston import Glasston
from SalaEnsamble import Ensamble
from ChillerP2 import Chiller
from DeshumedecedoresP2 import Deshumedecedores
from ACV import ACV1
#import pywhatkit

#----------------- Inicio --------------------#

options=webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/adminscada/AppData/Local/Google/ChromeUser Data")
#driver=webdriver.Chrome('chromedriver.exe',chrome_options=options)
browser = webdriver.Chrome(executable_path="C:/Python39/Scripts/chromedriver",chrome_options=options)
browser.get("https://web.whatsapp.com/")
wait = WebDriverWait(browser,800)


#----------------- Variables Iniciales --------------------#
m = 0 

y = [0,0,0,0,0,0,0,0,0,0]

w = [0,0,0,0,0,0,0,0,0,0] 

mensajes  = []  # Listado Alarmas DB170
mensajes1 = [] # Listado Alarmas DB15
mensajes2 = [] # Listado Alarmas Osmosis
mensajes3 = [] # Listado Alarmas Ensamble
mensajes4 = "Aviso: Bot Operativo - Online"
mensajes5 = [] # Listado Alarmas Chiller
mensajes6 = [] # Listado Alarmas Energia
mensajes7 = [] # Listado Alarmas Lavadoras
mensajes8 = "Bot: Lavadora Curva-ALARMA: Filtro Aire"
mensajes9 = [] # Listado Alarmas Deshumedecedores
#mensajes10 = "Bot: Horno Glasston - ALARMA: SobreTemperatura Modulo RK8" 
mensajes10 = []
mensajes11 = "Bot: Autoclave-ALARMA: Revisar"
#contacto1 = '"Pruebas y Mas"'
contacto1 = '"Javier"'
contacto = '"Alarmas_Equipos_Planta2"'

#----------------- Lectura de Mensajes -------------------#

#----------------- Mensajes Glasston DB170 -------------------#

mensajes = MensajesAlarmas("C:/Users/adminscada/Desktop/python/datos.txt", mensajes)

#----------------- Mensajes Glasston DB15 -------------------#

mensajes1 = MensajesAlarmas("C:/Users/adminscada/Desktop/python/AlarmasGlaston.txt", mensajes1)

#----------------- Mensajes Osmosis -------------------#

mensajes2 = MensajesAlarmas("C:/Users/adminscada/Desktop/python/AlarmasOsmosis.txt", mensajes2)

#----------------- Mensajes Ensamble -------------------#

mensajes3 = MensajesAlarmas("C:/Users/adminscada/Desktop/python/AlarmasEnsamble.txt", mensajes3)

#----------------- Mensajes Chiller -------------------#

mensajes5 = MensajesAlarmas("C:/Users/adminscada/Desktop/python/AlarmasChiller.txt", mensajes5)

#----------------- Mensajes Consumo Potencia Equipos -------------------#

mensajes6 = MensajesAlarmas("C:/Users/adminscada/Desktop/python/AlarmasEnergia.txt", mensajes6)

#----------------- Mensajes Lavadoras P2 -------------------#

mensajes7 = MensajesAlarmas("C:/Users/adminscada/Desktop/python/AlarmasLavadorasP2.txt", mensajes7)

#----------------- Mensajes Deshumedecedores -------------------#

mensajes9 = MensajesAlarmas("C:/Users/adminscada/Desktop/python/AlarmasDeshumedecedores.txt", mensajes9)

#----------------- Mensajes Glasston Modulos RK -------------------#

mensajes10 = MensajesAlarmas("C:/Users/adminscada/Desktop/python/AlarmasRKGlasston.txt", mensajes10)


#----------------- Metodos --------------------#

def sendAviso1(data, byte, bit, contacto, mensaje, n):
	global w
	global wait
	#global browser

	Alarm7 = get_bool(data,byte,bit)

	if Alarm7 == False and w[n] == 0:
		try:
			w[n] = 1
			#pywhatkit.sendwhatmsg_to_group_instantly("L1n0zzsjhxf7DA19pRRIDp",mensaje,14,True,20)
			grupo_path = '//span[contains(@title,'+ contacto +')]'
			grupo = wait.until(EC.presence_of_element_located((By.XPATH,grupo_path)))
			grupo.click()
			message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
			message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
			message_box.send_keys(mensaje + Keys.ENTER)
			print("Valor:", w[n])
			print(mensaje)

		except:
			w[n] = 0
			print("error en el envio")
			print(w[n])
	elif Alarm7 == True:
		w[n] = 0
		print("fin")

def sendAvisoPotencia(equipo, IP, ID, dato, m, n, contacto, mensaje):
	global y
	global wait

	equipo = ModbusClient(host = IP, port = 502, unit_id = ID, auto_open = True, debug = False)
	equipo_Online = equipo.open()
	print("Medidor en Linea:", equipo_Online)

	if equipo_Online == False:
		equipo = ModbusClient(host = IP, port = 502, unit_id = ID, auto_open = True, debug = False)

	regs1 = equipo.read_input_registers(20522,2)

	if IP == '10.52.5.184':
		try:
			Alarm2 = regs1[m]
			print(Alarm2)
		except:
			print("Linea except")
			Alarm2 = 0

	else:
		try:
			Alarm2 = regs1[m]/10
			print(Alarm2)
		except:
			print("Linea except")
			Alarm2 = 0

	if Alarm2 > dato and y[n] == 0:
		try:
			y[n] = 1
			grupo_path = '//span[contains(@title,'+ contacto +')]'
			grupo = wait.until(EC.presence_of_element_located((By.XPATH,grupo_path)))
			grupo.click()
			message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
			message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
			message_box.send_keys(mensaje + Keys.ENTER)
			print("Valor:", y[n])
			print(mensaje)

		except:
			y[n] = 0
			print("error en el envio")
			print(y[n])
	elif Alarm2 < dato:
		y[n] = 0
		print("fin")

def sendAvisoPotencia1(equipo, IP, ID, dato, n, contacto, mensaje):
	global y
	global wait

	equipo = ModbusClient(host = IP, port = 502, unit_id = ID, auto_open = True, debug = False)
	equipo_Online = equipo.open()
	print("Medidor en Linea:", equipo_Online)

	if equipo_Online == False:
		equipo = ModbusClient(host = IP, port = 502, unit_id = ID, auto_open = True, debug = False)

	try:		
		regs2  = equipo.read_input_registers(20480,20)
		Alarm3 = regs2
		print(Alarm3)
		if Alarm3 is None:
			print("Linea None")
			Alarm3[1]  = 0
			Alarm3[2]  = 0
			Alarm3[3]  = 0
			Alarm3[14] = 0
			Alarm3[15] = 0
			Alarm3[16] = 0

	except:
		print("Linea except")
		Alarm3[1]  = 0
		Alarm3[2]  = 0
		Alarm3[3]  = 0
		Alarm3[14] = 0
		Alarm3[15] = 0
		Alarm3[16] = 0

	sumaVoltajes   = (Alarm3[14] + Alarm3[15] + Alarm3[16])/30
	sumaCorrientes = (Alarm3[1] + Alarm3[2] + Alarm3[3])/3

	Potencia = round((sumaVoltajes*sumaCorrientes*1.7320)/1000,3) 
	print(Potencia)

	if Potencia > dato and y[n] == 0:
		try:
			y[n] = 1
			grupo_path = '//span[contains(@title,'+ contacto +')]'
			grupo = wait.until(EC.presence_of_element_located((By.XPATH,grupo_path)))
			grupo.click()
			message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
			message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
			message_box.send_keys(mensaje + Keys.ENTER)
			print("Valor:", y[n])
			print(mensaje)

		except:
			y[n] = 0
			print("error en el envio")
			print(y[n])
	elif Potencia < dato:
		y[n] = 0
		print("fin")

def sendAvisoPotencia2(equipo1, equipo2, IP, ID1, ID2, dato, m, n, contacto, mensaje):
	global y
	global wait

	equipo1 = ModbusClient(host = IP, port = 502, unit_id = ID1, auto_open = True, debug = False)
	equipo1_Online = equipo1.open()
	print("Medidor en Linea GlasstonA:", equipo1_Online)

	if equipo1_Online == False:
		equipo1 = ModbusClient(host = IP, port = 502, unit_id = ID1, auto_open = True, debug = False)

	equipo2 = ModbusClient(host = IP, port = 502, unit_id = ID2, auto_open = True, debug = False)
	equipo2_Online = equipo2.open()
	print("Medidor en Linea GlasstonB:", equipo2_Online)

	if equipo2_Online == False:
		equipo2 = ModbusClient(host = IP, port = 502, unit_id = ID2, auto_open = True, debug = False)
	try:
		regs3 = equipo2.read_input_registers(20522,2)
		Alarm4 = regs3[m]/10
		print("Potencia GlasstonA:",Alarm4)
	except:
		Alarm4 = 0
		print("Linea except: ", Alarm4)
	try:

		regs4 = equipo1.read_input_registers(20480,20)
		Alarm5 = regs4
		print(Alarm5)
		if Alarm5 is None:
			print("Linea None")
			Alarm5[0]  = 0
			Alarm5[1]  = 0
			Alarm5[2]  = 0
			Alarm5[14] = 0
			Alarm5[15] = 0
			Alarm5[16] = 0

	except:
		print("Linea except")
		Alarm5[0]  = 0
		Alarm5[1]  = 0
		Alarm5[2]  = 0
		Alarm5[14] = 0
		Alarm5[15] = 0
		Alarm5[16] = 0

	sumaVoltajes   = (Alarm5[14] + Alarm5[15] + Alarm5[16])/30
	sumaCorrientes = (Alarm5[0] + Alarm5[1] + Alarm5[2])/3

	Potencia = round((sumaVoltajes*sumaCorrientes*1.7320)/1000,3) 
	print("Potencia GlasstonB:", Potencia)

	PotenciaTotal= Potencia + Alarm4
	print("PotenciaTotal:", PotenciaTotal)

	if PotenciaTotal > dato and y[n] == 0:
		try:
			y[n] = 1
			grupo_path = '//span[contains(@title,'+ contacto +')]'
			grupo = wait.until(EC.presence_of_element_located((By.XPATH,grupo_path)))
			grupo.click()
			message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
			message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
			message_box.send_keys(mensaje + Keys.ENTER)
			print("Valor:", y[n])
			print(mensaje)

		except:
			y[n] = 0
			print("error en el envio")
			print(y[n])
	elif PotenciaTotal < dato:
		y[n] = 0
		print("fin")	

def sendAvisoLavadorasP2(data, byte, EN, contacto, mensaje, n, caudal):
	global w
	global wait
	#global browser
	if EN == 0:
		Alarm6 = get_real(data,byte)

	elif EN == 1:
		Alarm6 = get_word(data,byte)

	elif EN == 2:
		regs5 = plcLavadoraPlana2.read_holding_registers(byte,2)
		Alarm6 = regs5[0]

	if Alarm6 > caudal and w[n] == 0:
		try:
			w[n] = 1
			#pywhatkit.sendwhatmsg_to_group_instantly("L1n0zzsjhxf7DA19pRRIDp",mensaje,14,True,20)
			grupo_path = '//span[contains(@title,'+ contacto +')]'
			grupo = wait.until(EC.presence_of_element_located((By.XPATH,grupo_path)))
			grupo.click()
			message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
			message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
			message_box.send_keys(mensaje + Keys.ENTER)
			print("Valor:", w[n])
			print(mensaje)

		except:
			w[n] = 0
			print("error en el envio")
			print(w[n])
	elif Alarm6 < caudal:
		w[n] = 0
		print("fin")

def controlTime(mensaje,contacto,hora):
	global m
	if (hora == "00:00" or hora == "06:00" or hora == "12:00" or hora == "18:00") and m == 0:
		try:
			m = 1
			grupo_path = '//span[contains(@title,'+ contacto +')]'
			grupo = wait.until(EC.presence_of_element_located((By.XPATH,grupo_path)))
			grupo.click()
			message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
			message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
			message_box.send_keys(mensaje + Keys.ENTER)
			print("Valor:", m)
			print(mensaje)

		except:
			m = 0
			print("error en el envio")
			print(m)
	elif hora != "00:00" and hora != "06:00" and hora != "12:00" and hora != "18:00":
		m = 0
		print("Estoy aca")

	#----------------- Conexion Horno Glasston --------------------#
try:		

	plcGlaston = c.Client()
	plcGlaston.connect('192.168.107.9',0,3) 

	#----------------- Conexion Horno Glasston - Estatus --------------------#
	Estatus = plcGlaston.get_cpu_state()
	print("Estatus PLC :", Estatus)

	En_Linea = plcGlaston.get_connected()
	print("PLC Online:", En_Linea)

except:
	En_Linea = False

#----------------- Conexion Osmosis --------------------#
try:
	
	plcOsmosis = ModbusClient(host = '10.52.5.187', port = 502, auto_open = True, debug = False)
	Osmosis_Online = plcOsmosis.open()

	print("Osmosis en Linea:", Osmosis_Online)

except:
	Osmosis_Online = False

	#----------------- Conexion PLC Ensamble --------------------#
try:

	comm = PLC()
	comm.IPAddress = '10.52.5.100'
	Ensamble_Online = comm.conn.connect()
	print("Ensamble en Linea:", Ensamble_Online[0])
except:
	Ensamble_Online = comm.conn.connect()

#----------------- Conexion PLC Chiller --------------------#
try:
	
	comm1 = PLC()
	comm1.IPAddress = '10.52.5.51'
	Chiller_Online = comm1.conn.connect()
	print("Chiller en Linea:", Chiller_Online[0])
except:
	Chiller_Online = comm1.conn.connect()

	#----------------- Conexion LavadoraPlana --------------------#
"""try:
	plcLavadoraPlana = c.Client()
	plcLavadoraPlana.connect('10.52.5.25',0,2) 

	#----------------- Conexion LavadoraPlana - Estatus --------------------#
	Estatus1 = plcLavadoraPlana.get_cpu_state()
	print("Estatus PLC :", Estatus1)

	En_Linea1 = plcLavadoraPlana.get_connected()
	print("PLC Online:", En_Linea1)
except:
	En_Linea1 = False

	#----------------- Conexion LavadoraPlana3 --------------------#
try:
	plcLavadoraPlana3 = c.Client()
	plcLavadoraPlana3.connect('10.52.5.190',0,2) 

	#----------------- Conexion LavadoraPlana3 - Estatus --------------------#
	Estatus3 = plcLavadoraPlana3.get_cpu_state()
	print("Estatus PLC :", Estatus3)

	En_Linea3 = plcLavadoraPlana3.get_connected()
	print("PLC Online:", En_Linea3)

except:
	En_Linea3 = False

	#----------------- Conexion LavadoraPlana2 - Estatus --------------------#
try:	
	plcLavadoraPlana2 = ModbusClient(host = '10.52.5.189', port = 502, auto_open = True, debug = False)
	LavadoraPlana2_Online = plcLavadoraPlana2.open()

	print("LavadoraPlana2 en Linea:", LavadoraPlana2_Online)

except:
	LavadoraPlana2_Online = False"""

	#----------------- Conexion ACV --------------------#
try:

	plcACV = ModbusClient(host = '10.52.5.140', port = 502, auto_open = True, debug = False)
	ACV_Online = plcACV.open()

	print("ACV en Linea:", ACV_Online)

except:
	ACV_Online = False

#----------------- Conexion Deshumedecedores --------------------#
try:
	
	plcDeshumedecedores = ModbusClient(host = '10.52.5.105', port = 502, auto_open = True, debug = False)
	Deshumedecedores_Online = plcDeshumedecedores.open()

	print("Deshumedecedores en Linea:", Deshumedecedores_Online)
except:
	Deshumedecedores_Online = False

#----------------- Conexion LavadoraCurva --------------------#
try:
	
	plcLavadoraCurva = c.Client()
	plcLavadoraCurva.connect('10.52.5.95',0,2) 

	#----------------- Conexion LavadoraCurva - Estatus --------------------#
	Estatus2 = plcLavadoraCurva.get_cpu_state()
	print("Estatus PLC :", Estatus2)

	En_Linea2 = plcLavadoraCurva.get_connected()
	print("PLC Online:", En_Linea2)
except:
	En_Linea2 = False

#---------------------- Inicio Ciclo -------------------------#

while True:

	#print("LavadoraPlana en Linea:", En_Linea1)
	print("LavadoraCurva en Linea:", En_Linea2)
	#print("LavadoraPlana3 en Linea:", En_Linea3)
	#print("LavadoraPlana2 en Linea:", LavadoraPlana2_Online)


#----------------- Generacion de Mensajes --------------------#
	

#----------------- PLC Glasston -----------------------#
	Glasston(En_Linea,plcGlaston,mensajes,mensajes1,mensajes10,contacto,wait)

#----------------- PLC Proface Osmosis -----------------------#

	Osmosis(Osmosis_Online,mensajes2,plcOsmosis,contacto,wait)	

#----------------- PLC Ensamble -----------------------#
	
	Ensamble(Ensamble_Online,comm,mensajes3,contacto,wait)

#----------------- PLC Chiller -----------------------#

	Chiller(Chiller_Online,comm1,mensajes5,contacto,wait)

#----------------- PLC LavadoraPlana -----------------------#
	#if En_Linea1 == False:
	#	plcLavadoraPlana = c.Client()
	#	plcLavadoraPlana.connect('10.52.5.25',0,2)

#----------------- PLC LavadoraCurva -----------------------#
	if En_Linea2 == False:
		try:
			plcLavadoraCurva = c.Client()
			plcLavadoraCurva.connect('10.52.5.95',0,2)
		except:
			En_Linea2 == False
			print("LavadoraCurva: ", En_Linea2)	

#----------------- PLC LavadoraPlana3 -----------------------#
	"""if En_Linea3 == False:
		plcLavadoraPlana3 = c.Client()
		plcLavadoraPlana3.connect('10.52.5.190',0,2)

	if LavadoraPlana2_Online == False:
		plcLavadoraPlana2 = ModbusClient(host = '10.52.5.189', port = 502, auto_open = True, debug = False)"""

	#----------------- PLC Proface Deshumedecedores -----------------------#

	Deshumedecedores(Deshumedecedores_Online,mensajes9,plcDeshumedecedores,contacto,wait)

	#----------------- PLC Proface ACV1 -----------------------#

	ACV1(ACV_Online,mensajes11,plcACV,contacto,wait)
	

#------------------ Envio de Avisos a Whatsapp ----------------------#
#------------------ Mensajes Datos ----------------------#
	hora = datetime.now()
	fecha = datetime.today()
	horaActual = hora.strftime("%H:%M")
	fechaActual = fecha.strftime("%d/%m/%Y")
	print(horaActual)
	print(fechaActual)
	if fechaActual == "24/12/2022" or fechaActual == "25/12/2022" or fechaActual == "31/12/2022" or fechaActual == "01/01/2023":
		controlTime(mensajes4, contacto,horaActual)

	else:
		controlTime(mensajes4,contacto1,horaActual)

#------------------ Envio de Avisos a Whatsapp ----------------------#
	try:
		print("Hola")
	
		#sendAvisoPotencia("HornoHumam",'10.52.5.182',26, 10000.0,0,3,contacto,mensajes6[3])
		#sendAvisoPotencia("SalaEnsamble",'10.52.5.182',31, 10000.0,0,4,contacto,mensajes6[4])
		#sendAvisoPotencia("Autoclave",'10.52.5.182',42, 10000.0,0,0,contacto,mensajes6[0])
		#sendAvisoPotencia("LavadoraCurva",'10.52.5.182',25,10000.0,0,5,contacto,mensajes6[5])
		#sendAvisoPotencia("HornoIOX",'10.52.5.184',11,10000.0,0,6,contacto,mensajes6[6])
	except HornoVitrificado:	
		sendAvisoPotencia1("HornoVitrificado",'10.52.5.184',16,600.0,7,contacto,mensajes6[7])
	except HornoEcomax:	
		sendAvisoPotencia1("HornoEcomax",'10.52.5.184',12,900.0,2,contacto,mensajes6[2])
	except HornoGlasston:
		sendAvisoPotencia2("HornoGlasstonA","HornoGlasstonB",'10.52.5.182',24,22,1200.0,0,1,contacto,mensajes6[1])

	#sendAvisoPotencia("HornoHumam",'10.52.5.182',26, 10000.0,0,3,contacto,mensajes6[3])
	#sendAvisoPotencia("SalaEnsamble",'10.52.5.182',31, 10000.0,0,4,contacto,mensajes6[4])
	#sendAvisoPotencia("Autoclave",'10.52.5.182',42, 10000.0,0,0,contacto,mensajes6[0])
	#sendAvisoPotencia("LavadoraCurva",'10.52.5.182',25,10000.0,0,5,contacto,mensajes6[5])
	#sendAvisoPotencia("HornoIOX",'10.52.5.184',11,10000.0,0,6,contacto,mensajes6[6])
	sendAvisoPotencia1("HornoVitrificado",'10.52.5.184',16,600.0,7,contacto,mensajes6[7])
	sendAvisoPotencia1("HornoEcomax",'10.52.5.184',12,900.0,2,contacto,mensajes6[2])
	sendAvisoPotencia2("HornoGlasstonA","HornoGlasstonB",'10.52.5.182',24,22,1200.0,0,1,contacto,mensajes6[1])

	"""try:
		datos = plcLavadoraPlana.read_area(Areas['DB'],1,0,16)
	except:
		sendAvisoLavadorasP2(datos,12,0,contacto,mensajes7[0],0,3000)

	sendAvisoLavadorasP2(datos,12,0,contacto,mensajes7[0],0,3000)"""

	if En_Linea2 == True:

		try:
			datos1 = plcLavadoraCurva.read_area(Areas['DB'],1,0,16)
			datos3 = plcLavadoraCurva.read_area(Areas['PE'],0,5,1)
			print("Javier")
		except:
			sendAvisoLavadorasP2(datos1,12,0,contacto,mensajes7[1],1,3000)
			sendAviso1(datos3,0,3,contacto,mensajes8,4)
				
		sendAvisoLavadorasP2(datos1,12,0,contacto,mensajes7[1],1,3000)
		sendAviso1(datos3,0,3,contacto,mensajes8,4)

	else:
		print("Fallo en la comunicacion")
		En_Linea2 = False

	"""try:
		datos2 = plcLavadoraPlana3.read_area(Areas['MK'],0,196,2)
	except:
		sendAvisoLavadorasP2(datos2,0,1,contacto,mensajes7[2],2,3000)

	sendAvisoLavadorasP2(datos,0,1,contacto,mensajes7[2],2,3000)

	try:
		print("LavadoraPlana2")
	except:
		sendAvisoLavadorasP2("Hola",0,2,contacto,mensajes7[3],3,3000)

	sendAvisoLavadorasP2("Hola",0,2,contacto,mensajes7[3],3,3000)"""

		
#------------------- Retardo de 5 segundos ----------------------#
	sleep(10)
	


