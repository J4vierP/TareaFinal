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
import snap7.client as c
from snap7.util import *
from snap7.types import *
#from snap7.snap7types import *
import ctypes
from ctypes import *
from enum import Enum
from snap7.common import ADict
from time import sleep
#import pywhatkit

#----------------- Inicio --------------------#

options=webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/adminscada/AppData/Local/Google/ChromeUser Data")
#driver=webdriver.Chrome('chromedriver.exe',chrome_options=options)
browser = webdriver.Chrome(executable_path="C:/Python39/Scripts/chromedriver",chrome_options=options)
browser.get("https://web.whatsapp.com/")
wait = WebDriverWait(browser,600)


#----------------- Variables Iniciales --------------------#
i = [
	 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	]
j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]	
mensajes = []  # Listado Alarmas DB170
mensajes1 = [] # Listado Alarmas DB15
mensajes2 = [] # Listado Alarmas Osmosis
#contacto1 = '"Pruebas y Mas"'
contacto = '"TURNO MANT. UNIDAD 3,4y5"'
#----------------- Lectura de Mensajes -------------------#
f = open("C:/Users/adminscada/Desktop/python/datos.txt","r")
data2 = f.readlines()
f.close()
print(data2)
for line in data2:
	mensajes.append(line.rstrip())
	print(line.rstrip())
print(mensajes[0])
print(mensajes[1])

f1 = open("C:/Users/adminscada/Desktop/python/AlarmasGlaston.txt","r")
data3 = f1.readlines()
f1.close()
print(data3)
for line1 in data3:
	mensajes1.append(line1.rstrip())
	print(line1.rstrip())
print(mensajes1[0])
print(mensajes1[1])

f2 = open("C:/Users/adminscada/Desktop/python/AlarmasOsmosis.txt","r")
data4 = f2.readlines()
f2.close()
print(data4)
for line2 in data4:
	mensajes2.append(line2.rstrip())
	print(line2.rstrip())
print(mensajes2[0])
print(mensajes2[1])

#----------------- Metodos --------------------#
def ReadMemory(plc,byte,bit,datatype):
    result = plc.read_area(Areas['MK'],0,byte,datatype)
    if datatype==S7WLBit:
       	return get_bool(result,0,bit)
    elif datatype== S7WLByte or datatype== S7WLWord:
    	return get_int(result,0)
    elif datatype==S7WLReal:
        return get_real(result,0)
    elif datatype==S7WLDWord:
        return get_dword(result,0)
    else:
        return None
def sendAviso(data, byte, bit, contacto, mensaje, n):
	global i
	global wait
	#global browser

	Alarm1 = get_bool(data,byte,bit)

	if Alarm1 == True and i[n] == 0:
		try:
			i[n] = 1
			#pywhatkit.sendwhatmsg_to_group_instantly("L1n0zzsjhxf7DA19pRRIDp",mensaje,14,True,20)
			grupo_path = '//span[contains(@title,'+ contacto +')]'
			grupo = wait.until(EC.presence_of_element_located((By.XPATH,grupo_path)))
			grupo.click()
			message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
			message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
			message_box.send_keys(mensaje + Keys.ENTER)
			print("Valor:", i[n])
			print(mensaje)

		except:
			i[n] = 0
			print("error en el envio")
			print(i[n])
	elif Alarm1 == False:
		i[n] = 0
		print("fin")
def sendAvisoOsmosis(m, n, p, contacto, mensaje):
	global j
	global wait
	#regs = registro
	regs = plcOsmosis.read_holding_registers(9,2)
	Alarm2 = regs[m]
	print(Alarm2)

	if Alarm2 == p and j[n] == 0:
		print("estoy aca")
		try:
			j[n] = 1
			print(j[n])
			#pywhatkit.sendwhatmsg_to_group_instantly("L1n0zzsjhxf7DA19pRRIDp",mensaje,14,True,20)
			grupo_path = '//span[contains(@title,'+ contacto +')]'
			grupo = wait.until(EC.presence_of_element_located((By.XPATH,grupo_path)))
			grupo.click()
			message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
			message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
			message_box.send_keys(mensaje + Keys.ENTER)
			print("Valor:", j[n])
			print(mensaje)

		except:
			j[n] = 0
			print("error en el envio")
			print(j[n])
	elif Alarm2 != p:
		j[n] = 0
		print("fin")
		
#----------------- Conexion Horno Glasston --------------------#
plcGlaston = c.Client()
plcGlaston.connect('192.168.107.9',0,3) 

#----------------- Conexion Horno Glasston - Estatus --------------------#
Estatus = plcGlaston.get_cpu_state()
print("Estatus PLC :", Estatus)

En_Linea = plcGlaston.get_connected()
print("PLC Online:", En_Linea)

#----------------- Conexion Osmosis --------------------#
plcOsmosis = ModbusClient(host = '10.52.5.187', port = 502, auto_open = True, debug = False)
Osmosis_Online = plcOsmosis.open()

print("Osmosis en Linea:", Osmosis_Online)

#---------------------- Inicio Ciclo -------------------------#

while True:

	print ("En Linea", En_Linea)
	print("Osmosis en Linea:", Osmosis_Online)

#----------------- Generacion de Mensajes --------------------#
	

#----------------- Verificacion de Comunicacion con el PLC -----------------------#
	if En_Linea == False:
		plcGlaston = c.Client()
		plcGlaston.connect('192.168.107.9',0,3) #estructura metodo connect: plcGlaston.connect('IP del PLC', Rack , slot)
		#plcGlaston.connect('192.168.0.10',0,1)
#----------------- Verificacion de Comunicacion con el PLC -----------------------#
	if Osmosis_Online == False:
		plcOsmosis = ModbusClient(host = '10.52.5.187', port = 502, auto_open = True, debug = False)


#------------------ Lectura Datos DB170 y DB15----------------------#
	try:
		data = plcGlaston.read_area(Areas['DB'],170,0,6)	
		data1 = plcGlaston.read_area(Areas['DB'],15,0,18)
		print("try")

	except:
#------------------ Mensajes Datos DB15----------------------#
		sendAviso(data1,0,0,contacto,mensajes1[0],0)
		sendAviso(data1,0,1,contacto,mensajes1[1],1)	
		sendAviso(data1,0,2,contacto,mensajes1[2],2)	
		sendAviso(data1,0,3,contacto,mensajes1[3],3)	
		sendAviso(data1,0,4,contacto,mensajes1[4],4)	
		sendAviso(data1,0,5,contacto,mensajes1[5],5)
		sendAviso(data1,0,6,contacto,mensajes1[6],6)
		sendAviso(data1,0,7,contacto,mensajes1[7],7)
		sendAviso(data1,1,0,contacto,mensajes1[8],8)
		sendAviso(data1,1,1,contacto,mensajes1[9],9)	
		sendAviso(data1,1,2,contacto,mensajes1[10],10)	
		sendAviso(data1,1,3,contacto,mensajes1[11],11)	
		sendAviso(data1,1,4,contacto,mensajes1[12],12)	
		sendAviso(data1,1,5,contacto,mensajes1[13],13)
		sendAviso(data1,1,6,contacto,mensajes1[14],14)
		sendAviso(data1,1,7,contacto,mensajes1[15],15)
		sendAviso(data1,2,0,contacto,mensajes1[16],16)
		sendAviso(data1,2,1,contacto,mensajes1[17],17)	
		sendAviso(data1,2,2,contacto,mensajes1[18],18)	
		sendAviso(data1,2,3,contacto,mensajes1[19],19)	
		sendAviso(data1,2,4,contacto,mensajes1[20],20)	
		sendAviso(data1,2,5,contacto,mensajes1[21],21)
		sendAviso(data1,2,6,contacto,mensajes1[22],22)
		sendAviso(data1,2,7,contacto,mensajes1[23],23)
		sendAviso(data1,3,0,contacto,mensajes1[24],24)
		sendAviso(data1,3,1,contacto,mensajes1[25],25)	
		sendAviso(data1,3,2,contacto,mensajes1[26],26)	
		sendAviso(data1,3,3,contacto,mensajes1[27],27)	
		sendAviso(data1,3,4,contacto,mensajes1[28],28)	
		sendAviso(data1,3,5,contacto,mensajes1[29],29)
		sendAviso(data1,3,6,contacto,mensajes1[30],30)
		sendAviso(data1,3,7,contacto,mensajes1[31],31)
		sendAviso(data1,4,0,contacto,mensajes1[32],32)
		sendAviso(data1,4,1,contacto,mensajes1[33],33)	
		sendAviso(data1,4,2,contacto,mensajes1[34],34)	
		sendAviso(data1,4,3,contacto,mensajes1[35],35)	
		sendAviso(data1,4,4,contacto,mensajes1[36],36)	
		sendAviso(data1,4,5,contacto,mensajes1[37],37)
		sendAviso(data1,4,6,contacto,mensajes1[38],38)
		sendAviso(data1,4,7,contacto,mensajes1[39],39)
		sendAviso(data1,5,0,contacto,mensajes1[40],40)
		sendAviso(data1,5,1,contacto,mensajes1[41],41)	
		sendAviso(data1,5,2,contacto,mensajes1[42],42)	
		sendAviso(data1,5,3,contacto,mensajes1[43],43)	
		sendAviso(data1,5,4,contacto,mensajes1[44],44)	
		sendAviso(data1,5,5,contacto,mensajes1[45],45)
		sendAviso(data1,5,6,contacto,mensajes1[46],46)
		sendAviso(data1,5,7,contacto,mensajes1[47],47)
		sendAviso(data1,6,0,contacto,mensajes1[48],48)
		sendAviso(data1,6,1,contacto,mensajes1[49],49)	
		sendAviso(data1,6,2,contacto,mensajes1[50],50)	
		sendAviso(data1,6,3,contacto,mensajes1[51],51)	
		sendAviso(data1,6,4,contacto,mensajes1[52],52)	
		sendAviso(data1,6,5,contacto,mensajes1[53],53)
		sendAviso(data1,6,6,contacto,mensajes1[54],54)
		sendAviso(data1,6,7,contacto,mensajes1[55],55)
		sendAviso(data1,7,0,contacto,mensajes1[56],56)
		sendAviso(data1,7,1,contacto,mensajes1[57],57)	
		sendAviso(data1,7,2,contacto,mensajes1[58],58)	
		sendAviso(data1,7,3,contacto,mensajes1[59],59)	
		sendAviso(data1,7,4,contacto,mensajes1[60],60)	
		sendAviso(data1,7,5,contacto,mensajes1[61],61)
		sendAviso(data1,7,6,contacto,mensajes1[62],62)
		sendAviso(data1,7,7,contacto,mensajes1[63],63)
		sendAviso(data1,8,0,contacto,mensajes1[64],64)
		sendAviso(data1,8,1,contacto,mensajes1[65],65)	
		sendAviso(data1,8,2,contacto,mensajes1[66],66)	
		sendAviso(data1,8,3,contacto,mensajes1[67],67)	
		sendAviso(data1,8,4,contacto,mensajes1[68],68)	
		sendAviso(data1,8,5,contacto,mensajes1[69],69)
		sendAviso(data1,8,6,contacto,mensajes1[70],70)
		sendAviso(data1,8,6,contacto,mensajes1[70],70)
		sendAviso(data1,8,7,contacto,mensajes1[71],71)
		sendAviso(data1,9,0,contacto,mensajes1[72],72)
		sendAviso(data1,9,1,contacto,mensajes1[73],73)	
		sendAviso(data1,9,2,contacto,mensajes1[74],74)	
		sendAviso(data1,9,3,contacto,mensajes1[75],75)	
		sendAviso(data1,9,4,contacto,mensajes1[76],76)	
		sendAviso(data1,9,5,contacto,mensajes1[77],77)
		sendAviso(data1,9,6,contacto,mensajes1[78],78)
		sendAviso(data1,9,7,contacto,mensajes1[79],79)
		sendAviso(data1,10,0,contacto,mensajes1[80],80)
		sendAviso(data1,10,1,contacto,mensajes1[81],81)	
		sendAviso(data1,10,2,contacto,mensajes1[82],82)	
		sendAviso(data1,10,3,contacto,mensajes1[83],83)	
		sendAviso(data1,10,4,contacto,mensajes1[84],84)	
		sendAviso(data1,10,5,contacto,mensajes1[85],85)
		sendAviso(data1,10,6,contacto,mensajes1[86],86)
		sendAviso(data1,10,7,contacto,mensajes1[87],87)
		sendAviso(data1,11,0,contacto,mensajes1[88],88)
		sendAviso(data1,11,1,contacto,mensajes1[89],89)	
		sendAviso(data1,11,2,contacto,mensajes1[90],90)	
		sendAviso(data1,11,3,contacto,mensajes1[91],91)	
		sendAviso(data1,11,4,contacto,mensajes1[92],92)	
		sendAviso(data1,11,5,contacto,mensajes1[93],93)
		sendAviso(data1,11,6,contacto,mensajes1[94],94)
		sendAviso(data1,11,7,contacto,mensajes1[95],95)
		sendAviso(data1,12,0,contacto,mensajes1[96],96)
		sendAviso(data1,12,1,contacto,mensajes1[97],97)	
		sendAviso(data1,12,2,contacto,mensajes1[98],98)	
		sendAviso(data1,12,3,contacto,mensajes1[99],99)	
		sendAviso(data1,12,4,contacto,mensajes1[100],100)	
		sendAviso(data1,12,5,contacto,mensajes1[101],101)
		sendAviso(data1,12,6,contacto,mensajes1[102],102)
		sendAviso(data1,12,7,contacto,mensajes1[103],103)
		sendAviso(data1,13,0,contacto,mensajes1[104],104)
		sendAviso(data1,13,1,contacto,mensajes1[105],105)	
		sendAviso(data1,13,2,contacto,mensajes1[106],106)	
		sendAviso(data1,13,3,contacto,mensajes1[107],107)	
		sendAviso(data1,13,4,contacto,mensajes1[108],108)	
		sendAviso(data1,13,5,contacto,mensajes1[109],109)
		sendAviso(data1,13,6,contacto,mensajes1[110],110)
		sendAviso(data1,13,7,contacto,mensajes1[111],111)
		sendAviso(data1,14,0,contacto,mensajes1[112],112)
		sendAviso(data1,14,1,contacto,mensajes1[113],113)	
		sendAviso(data1,14,2,contacto,mensajes1[114],114)	
		sendAviso(data1,14,3,contacto,mensajes1[115],115)	
		sendAviso(data1,14,4,contacto,mensajes1[116],116)	
		sendAviso(data1,14,5,contacto,mensajes1[117],117)
		sendAviso(data1,14,6,contacto,mensajes1[118],118)
		sendAviso(data1,14,7,contacto,mensajes1[119],119)
		sendAviso(data1,15,0,contacto,mensajes1[120],120)
		sendAviso(data1,15,1,contacto,mensajes1[121],121)	
		sendAviso(data1,15,2,contacto,mensajes1[122],122)	
		sendAviso(data1,15,3,contacto,mensajes1[124],123)	
		sendAviso(data1,15,4,contacto,mensajes1[125],125)	
		sendAviso(data1,15,5,contacto,mensajes1[126],126)
		sendAviso(data1,15,6,contacto,mensajes1[127],127)
		sendAviso(data1,15,7,contacto,mensajes1[128],128)
		sendAviso(data1,16,0,contacto,mensajes1[129],129)
		sendAviso(data1,16,1,contacto,mensajes1[130],130)	
		sendAviso(data1,16,2,contacto,mensajes1[131],131)	
		sendAviso(data1,16,3,contacto,mensajes1[132],132)	
		sendAviso(data1,16,4,contacto,mensajes1[133],133)	
		sendAviso(data1,16,5,contacto,mensajes1[134],134)
		sendAviso(data1,16,6,contacto,mensajes1[135],135)
		sendAviso(data1,16,7,contacto,mensajes1[136],136)
		sendAviso(data1,17,0,contacto,mensajes1[137],137)
		sendAviso(data1,17,1,contacto,mensajes1[138],138)	
		sendAviso(data1,17,2,contacto,mensajes1[139],139)	
		sendAviso(data1,17,3,contacto,mensajes1[140],140)	
		sendAviso(data1,17,4,contacto,mensajes1[141],141)
	
#------------------ Mensajes Datos DB170----------------------#
		sendAviso(data,2,1,contacto,mensajes[17],159)
		"""sendAviso(data,0,0,contacto,mensajes[0],142)
		sendAviso(data,0,1,contacto,mensajes[1],143)
		sendAviso(data,0,2,contacto,mensajes[2],144)
		sendAviso(data,0,3,contacto,mensajes[3],145)
		sendAviso(data,0,4,contacto,mensajes[4],146)
		sendAviso(data,0,5,contacto,mensajes[5],147)
		sendAviso(data,0,6,contacto,mensajes[6],148)
		sendAviso(data,0,7,contacto,mensajes[7],149)
		sendAviso(data,1,0,contacto,mensajes[8],150)
		sendAviso(data,1,1,contacto,mensajes[9],151)
		sendAviso(data,1,2,contacto,mensajes[10],152)
		sendAviso(data,1,3,contacto,mensajes[11],153)
		sendAviso(data,1,4,contacto,mensajes[12],154)
		sendAviso(data,1,5,contacto,mensajes[13],155)
		sendAviso(data,1,6,contacto,mensajes[14],156)
		sendAviso(data,1,7,contacto,mensajes[15],157)
		sendAviso(data,2,0,contacto,mensajes[16],158)
		sendAviso(data,2,1,contacto,mensajes[17],159)
		sendAviso(data,2,2,contacto,mensajes[18],160)
		sendAviso(data,2,3,contacto,mensajes[19],161)
		sendAviso(data,2,4,contacto,mensajes[20],162)
		sendAviso(data,2,5,contacto,mensajes[21],163)
		sendAviso(data,2,6,contacto,mensajes[22],164)
		sendAviso(data,2,7,contacto,mensajes[23],165)
		sendAviso(data,3,0,contacto,mensajes[24],166)
		sendAviso(data,3,1,contacto,mensajes[25],167)
		sendAviso(data,3,2,contacto,mensajes[26],168)
		sendAviso(data,3,3,contacto,mensajes[27],169)
		sendAviso(data,3,4,contacto,mensajes[28],170)
		sendAviso(data,3,5,contacto,mensajes[29],171)
		sendAviso(data,3,6,contacto,mensajes[30],172)
		sendAviso(data,3,7,contacto,mensajes[31],173)
		sendAviso(data,4,0,contacto,mensajes[32],174)
		sendAviso(data,4,1,contacto,mensajes[33],175)
		sendAviso(data,4,2,contacto,mensajes[34],176)
		sendAviso(data,4,3,contacto,mensajes[35],177)
		sendAviso(data,4,4,contacto,mensajes[36],178)
		sendAviso(data,4,5,contacto,mensajes[37],179)
		sendAviso(data,4,6,contacto,mensajes[38],180)
		sendAviso(data,4,7,contacto,mensajes[39],181)
		sendAviso(data,5,0,contacto,mensajes[40],182)
		sendAviso(data,5,1,contacto,mensajes[41],183)
		sendAviso(data,5,2,contacto,mensajes[42],184)"""
		
		print("Except")

	print(data)
	print(data1)
	print("Inicio")
	
#------------------ Envio de Avisos a Whatsapp ----------------------#
#------------------ Mensajes Datos DB15----------------------#
	sendAviso(data1,0,0,contacto,mensajes1[0],0)
	sendAviso(data1,0,1,contacto,mensajes1[1],1)	
	sendAviso(data1,0,2,contacto,mensajes1[2],2)	
	sendAviso(data1,0,3,contacto,mensajes1[3],3)	
	sendAviso(data1,0,4,contacto,mensajes1[4],4)	
	sendAviso(data1,0,5,contacto,mensajes1[5],5)
	sendAviso(data1,0,6,contacto,mensajes1[6],6)
	sendAviso(data1,0,7,contacto,mensajes1[7],7)
	sendAviso(data1,1,0,contacto,mensajes1[8],8)
	sendAviso(data1,1,1,contacto,mensajes1[9],9)	
	sendAviso(data1,1,2,contacto,mensajes1[10],10)	
	sendAviso(data1,1,3,contacto,mensajes1[11],11)	
	sendAviso(data1,1,4,contacto,mensajes1[12],12)	
	sendAviso(data1,1,5,contacto,mensajes1[13],13)
	sendAviso(data1,1,6,contacto,mensajes1[14],14)
	sendAviso(data1,1,7,contacto,mensajes1[15],15)
	sendAviso(data1,2,0,contacto,mensajes1[16],16)
	sendAviso(data1,2,1,contacto,mensajes1[17],17)	
	sendAviso(data1,2,2,contacto,mensajes1[18],18)	
	sendAviso(data1,2,3,contacto,mensajes1[19],19)	
	sendAviso(data1,2,4,contacto,mensajes1[20],20)	
	sendAviso(data1,2,5,contacto,mensajes1[21],21)
	sendAviso(data1,2,6,contacto,mensajes1[22],22)
	sendAviso(data1,2,7,contacto,mensajes1[23],23)
	sendAviso(data1,3,0,contacto,mensajes1[24],24)
	sendAviso(data1,3,1,contacto,mensajes1[25],25)	
	sendAviso(data1,3,2,contacto,mensajes1[26],26)	
	sendAviso(data1,3,3,contacto,mensajes1[27],27)	
	sendAviso(data1,3,4,contacto,mensajes1[28],28)	
	sendAviso(data1,3,5,contacto,mensajes1[29],29)
	sendAviso(data1,3,6,contacto,mensajes1[30],30)
	sendAviso(data1,3,7,contacto,mensajes1[31],31)
	sendAviso(data1,4,0,contacto,mensajes1[32],32)
	sendAviso(data1,4,1,contacto,mensajes1[33],33)	
	sendAviso(data1,4,2,contacto,mensajes1[34],34)	
	sendAviso(data1,4,3,contacto,mensajes1[35],35)	
	sendAviso(data1,4,4,contacto,mensajes1[36],36)	
	sendAviso(data1,4,5,contacto,mensajes1[37],37)
	sendAviso(data1,4,6,contacto,mensajes1[38],38)
	sendAviso(data1,4,7,contacto,mensajes1[39],39)
	sendAviso(data1,5,0,contacto,mensajes1[40],40)
	sendAviso(data1,5,1,contacto,mensajes1[41],41)	
	sendAviso(data1,5,2,contacto,mensajes1[42],42)	
	sendAviso(data1,5,3,contacto,mensajes1[43],43)	
	sendAviso(data1,5,4,contacto,mensajes1[44],44)	
	sendAviso(data1,5,5,contacto,mensajes1[45],45)
	sendAviso(data1,5,6,contacto,mensajes1[46],46)
	sendAviso(data1,5,7,contacto,mensajes1[47],47)
	sendAviso(data1,6,0,contacto,mensajes1[48],48)
	sendAviso(data1,6,1,contacto,mensajes1[49],49)	
	sendAviso(data1,6,2,contacto,mensajes1[50],50)	
	sendAviso(data1,6,3,contacto,mensajes1[51],51)	
	sendAviso(data1,6,4,contacto,mensajes1[52],52)	
	sendAviso(data1,6,5,contacto,mensajes1[53],53)
	sendAviso(data1,6,6,contacto,mensajes1[54],54)
	sendAviso(data1,6,7,contacto,mensajes1[55],55)
	sendAviso(data1,7,0,contacto,mensajes1[56],56)
	sendAviso(data1,7,1,contacto,mensajes1[57],57)	
	sendAviso(data1,7,2,contacto,mensajes1[58],58)	
	sendAviso(data1,7,3,contacto,mensajes1[59],59)	
	sendAviso(data1,7,4,contacto,mensajes1[60],60)	
	sendAviso(data1,7,5,contacto,mensajes1[61],61)
	sendAviso(data1,7,6,contacto,mensajes1[62],62)
	sendAviso(data1,7,7,contacto,mensajes1[63],63)
	sendAviso(data1,8,0,contacto,mensajes1[64],64)
	sendAviso(data1,8,1,contacto,mensajes1[65],65)	
	sendAviso(data1,8,2,contacto,mensajes1[66],66)	
	sendAviso(data1,8,3,contacto,mensajes1[67],67)	
	sendAviso(data1,8,4,contacto,mensajes1[68],68)	
	sendAviso(data1,8,5,contacto,mensajes1[69],69)
	sendAviso(data1,8,6,contacto,mensajes1[70],70)
	sendAviso(data1,8,6,contacto,mensajes1[70],70)
	sendAviso(data1,8,7,contacto,mensajes1[71],71)
	sendAviso(data1,9,0,contacto,mensajes1[72],72)
	sendAviso(data1,9,1,contacto,mensajes1[73],73)	
	sendAviso(data1,9,2,contacto,mensajes1[74],74)	
	sendAviso(data1,9,3,contacto,mensajes1[75],75)	
	sendAviso(data1,9,4,contacto,mensajes1[76],76)	
	sendAviso(data1,9,5,contacto,mensajes1[77],77)
	sendAviso(data1,9,6,contacto,mensajes1[78],78)
	sendAviso(data1,9,7,contacto,mensajes1[79],79)
	sendAviso(data1,10,0,contacto,mensajes1[80],80)
	sendAviso(data1,10,1,contacto,mensajes1[81],81)	
	sendAviso(data1,10,2,contacto,mensajes1[82],82)	
	sendAviso(data1,10,3,contacto,mensajes1[83],83)	
	sendAviso(data1,10,4,contacto,mensajes1[84],84)	
	sendAviso(data1,10,5,contacto,mensajes1[85],85)
	sendAviso(data1,10,6,contacto,mensajes1[86],86)
	sendAviso(data1,10,7,contacto,mensajes1[87],87)
	sendAviso(data1,11,0,contacto,mensajes1[88],88)
	sendAviso(data1,11,1,contacto,mensajes1[89],89)	
	sendAviso(data1,11,2,contacto,mensajes1[90],90)	
	sendAviso(data1,11,3,contacto,mensajes1[91],91)	
	sendAviso(data1,11,4,contacto,mensajes1[92],92)	
	sendAviso(data1,11,5,contacto,mensajes1[93],93)
	sendAviso(data1,11,6,contacto,mensajes1[94],94)
	sendAviso(data1,11,7,contacto,mensajes1[95],95)
	sendAviso(data1,12,0,contacto,mensajes1[96],96)
	sendAviso(data1,12,1,contacto,mensajes1[97],97)	
	sendAviso(data1,12,2,contacto,mensajes1[98],98)	
	sendAviso(data1,12,3,contacto,mensajes1[99],99)	
	sendAviso(data1,12,4,contacto,mensajes1[100],100)	
	sendAviso(data1,12,5,contacto,mensajes1[101],101)
	sendAviso(data1,12,6,contacto,mensajes1[102],102)
	sendAviso(data1,12,7,contacto,mensajes1[103],103)
	sendAviso(data1,13,0,contacto,mensajes1[104],104)
	sendAviso(data1,13,1,contacto,mensajes1[105],105)	
	sendAviso(data1,13,2,contacto,mensajes1[106],106)	
	sendAviso(data1,13,3,contacto,mensajes1[107],107)	
	sendAviso(data1,13,4,contacto,mensajes1[108],108)	
	sendAviso(data1,13,5,contacto,mensajes1[109],109)
	sendAviso(data1,13,6,contacto,mensajes1[110],110)
	sendAviso(data1,13,7,contacto,mensajes1[111],111)
	sendAviso(data1,14,0,contacto,mensajes1[112],112)
	sendAviso(data1,14,1,contacto,mensajes1[113],113)	
	sendAviso(data1,14,2,contacto,mensajes1[114],114)	
	sendAviso(data1,14,3,contacto,mensajes1[115],115)	
	sendAviso(data1,14,4,contacto,mensajes1[116],116)	
	sendAviso(data1,14,5,contacto,mensajes1[117],117)
	sendAviso(data1,14,6,contacto,mensajes1[118],118)
	sendAviso(data1,14,7,contacto,mensajes1[119],119)
	sendAviso(data1,15,0,contacto,mensajes1[120],120)
	sendAviso(data1,15,1,contacto,mensajes1[121],121)	
	sendAviso(data1,15,2,contacto,mensajes1[122],122)	
	sendAviso(data1,15,3,contacto,mensajes1[124],123)	
	sendAviso(data1,15,4,contacto,mensajes1[125],125)	
	sendAviso(data1,15,5,contacto,mensajes1[126],126)
	sendAviso(data1,15,6,contacto,mensajes1[127],127)
	sendAviso(data1,15,7,contacto,mensajes1[128],128)
	sendAviso(data1,16,0,contacto,mensajes1[129],129)
	sendAviso(data1,16,1,contacto,mensajes1[130],130)	
	sendAviso(data1,16,2,contacto,mensajes1[131],131)	
	sendAviso(data1,16,3,contacto,mensajes1[132],132)	
	sendAviso(data1,16,4,contacto,mensajes1[133],133)	
	sendAviso(data1,16,5,contacto,mensajes1[134],134)
	sendAviso(data1,16,6,contacto,mensajes1[135],135)
	sendAviso(data1,16,7,contacto,mensajes1[136],136)
	sendAviso(data1,17,0,contacto,mensajes1[137],137)
	sendAviso(data1,17,1,contacto,mensajes1[138],138)	
	sendAviso(data1,17,2,contacto,mensajes1[139],139)	
	sendAviso(data1,17,3,contacto,mensajes1[140],140)	
	sendAviso(data1,17,4,contacto,mensajes1[141],141)

#------------------ Mensajes Datos DB170----------------------#
	sendAviso(data,2,1,contacto,mensajes[17],159)
	"""sendAviso(data,0,0,contacto,mensajes[0],142)
	sendAviso(data,0,1,contacto,mensajes[1],143)
	sendAviso(data,0,2,contacto,mensajes[2],144)
	sendAviso(data,0,3,contacto,mensajes[3],145)
	sendAviso(data,0,4,contacto,mensajes[4],146)
	sendAviso(data,0,5,contacto,mensajes[5],147)
	sendAviso(data,0,6,contacto,mensajes[6],148)
	sendAviso(data,0,7,contacto,mensajes[7],149)
	sendAviso(data,1,0,contacto,mensajes[8],150)
	sendAviso(data,1,1,contacto,mensajes[9],151)
	sendAviso(data,1,2,contacto,mensajes[10],152)
	sendAviso(data,1,3,contacto,mensajes[11],153)
	sendAviso(data,1,4,contacto,mensajes[12],154)
	sendAviso(data,1,5,contacto,mensajes[13],155)
	sendAviso(data,1,6,contacto,mensajes[14],156)
	sendAviso(data,1,7,contacto,mensajes[15],157)
	sendAviso(data,2,0,contacto,mensajes[16],158)
	sendAviso(data,2,1,contacto,mensajes[17],159)
	sendAviso(data,2,2,contacto,mensajes[18],160)
	sendAviso(data,2,3,contacto,mensajes[19],161)
	sendAviso(data,2,4,contacto,mensajes[20],162)
	sendAviso(data,2,5,contacto,mensajes[21],163)
	sendAviso(data,2,6,contacto,mensajes[22],164)
	sendAviso(data,2,7,contacto,mensajes[23],165)
	sendAviso(data,3,0,contacto,mensajes[24],166)
	sendAviso(data,3,1,contacto,mensajes[25],167)
	sendAviso(data,3,2,contacto,mensajes[26],168)
	sendAviso(data,3,3,contacto,mensajes[27],169)
	sendAviso(data,3,4,contacto,mensajes[28],170)
	sendAviso(data,3,5,contacto,mensajes[29],171)
	sendAviso(data,3,6,contacto,mensajes[30],172)
	sendAviso(data,3,7,contacto,mensajes[31],173)
	sendAviso(data,4,0,contacto,mensajes[32],174)
	sendAviso(data,4,1,contacto,mensajes[33],175)
	sendAviso(data,4,2,contacto,mensajes[34],176)
	sendAviso(data,4,3,contacto,mensajes[35],177)
	sendAviso(data,4,4,contacto,mensajes[36],178)
	sendAviso(data,4,5,contacto,mensajes[37],179)
	sendAviso(data,4,6,contacto,mensajes[38],180)
	sendAviso(data,4,7,contacto,mensajes[39],181)
	sendAviso(data,5,0,contacto,mensajes[40],182)
	sendAviso(data,5,1,contacto,mensajes[41],183)
	sendAviso(data,5,2,contacto,mensajes[42],184)"""

#------------------ Lectura Datos Osmosis ----------------------#
	try:
		#regs = plcOsmosis.read_holding_registers(9,2)
		#print(regs)
		#print(regs[0])
		print("Try Osmosis")

	except:
		sendAvisoOsmosis(0,0,1,contacto,mensajes2[0])
		sendAvisoOsmosis(0,1,2,contacto,mensajes2[1])
		sendAvisoOsmosis(0,2,4,contacto,mensajes2[2])
		sendAvisoOsmosis(0,3,8,contacto,mensajes2[3])
		sendAvisoOsmosis(0,4,16,contacto,mensajes2[4])
		sendAvisoOsmosis(0,5,32,contacto,mensajes2[5])
		sendAvisoOsmosis(0,6,64,contacto,mensajes2[6])
		sendAvisoOsmosis(0,7,128,contacto,mensajes2[7])
		sendAvisoOsmosis(1,8,2,contacto,mensajes2[8])
		sendAvisoOsmosis(1,9,4,contacto,mensajes2[9])

#------------------ Envio de Avisos a Whatsapp ----------------------#
#------------------ Mensajes Datos Registros 10 y 11----------------------#
	#sendAvisoOsmosis()
	sendAvisoOsmosis(0,0,1,contacto,mensajes2[0])
	sendAvisoOsmosis(0,1,2,contacto,mensajes2[1])
	sendAvisoOsmosis(0,2,4,contacto,mensajes2[2])
	sendAvisoOsmosis(0,3,8,contacto,mensajes2[3])
	sendAvisoOsmosis(0,4,16,contacto,mensajes2[4])
	sendAvisoOsmosis(0,5,32,contacto,mensajes2[5])
	sendAvisoOsmosis(0,6,64,contacto,mensajes2[6])
	sendAvisoOsmosis(0,7,128,contacto,mensajes2[7])
	sendAvisoOsmosis(1,8,2,contacto,mensajes2[8])
	sendAvisoOsmosis(1,9,4,contacto,mensajes2[9])
	#sendAvisoOsmosis(0,5,32,contacto,mensajes2[5])



#------------------- Retardo de 5 segundos ----------------------#
	sleep(10)
	


