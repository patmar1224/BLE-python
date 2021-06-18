#!/usr/bin/python3 -u
#!/home/openhabian/Python3/Python-3.7.4/python -u
#-u to unbuffer output. Otherwise when calling with nohup or redirecting output things are printed very lately or would even mixup

from bluepy import btle
from dataclasses import dataclass
import traceback
import time
global measurements
import os

@dataclass
class Measurement:
	temperature: float
	humidity: int
	voltage: float
	battery: int = 0

measurement = Measurement(0,0,0,0)
sock = None #from ATC 
lastBLEPaketReceived = 0
#BLERestartCounter = 1
mode="round"

class MyDelegate(btle.DefaultDelegate):
	def __init__(self, params):
		btle.DefaultDelegate.__init__(self)
		# ... initialise here
	
	def handleNotification(self, cHandle, data): #Imprime los datos del sensor por pantalla y los guarda en la clase measurement
        
		#try:
			
		temp=int.from_bytes(data[0:2],byteorder='little',signed=True)/100
		humidity=int.from_bytes(data[2:3],byteorder='little')
		voltage=int.from_bytes(data[3:5],byteorder='little') / 1000.
		measurement.temperature = temp
		measurement.humidity = humidity
		measurement.voltage = voltage
		batteryLevel = min(int(round((voltage - 2.1),2) * 100), 100) #3.1 or above --> 100% 2.1 --> 0 %
		measurement.battery = batteryLevel

		#except Exception as e:
		#	print("Fehler")
		#	print(e)
		#	print(traceback.format_exc())
		
# Initialisation  -------

def connect(mac):
	#print("Interface: " + str(args.interface))
	p = btle.Peripheral(mac)	
	val=b'\x01\x00'
	p.writeCharacteristic(0x0038,val,True) #enable notifications of Temperature, Humidity and Battery voltage
	p.writeCharacteristic(0x0046,b'\xf4\x01\x00',True)
	p.withDelegate(MyDelegate("abc")) 
	return p

def Medida (mac):
    p=btle.Peripheral()
    connected=False
    if not connected:		
        #print("Trying to connect to A4:C1:38:52:09:5F")
        p=connect(mac)				
        connected=True
        p.waitForNotifications(2000)
				# handleNotification() was called
    crear_archivo() 
	
def crear_archivo():
    file=open("/home/pi/BLE-python/Cargar_datos_tabla.txt", "a")
    file.write(str(time.strftime('%d-%m-%Y')) + " , "+str(time.strftime("%H:%M:%S"))+", "+str(measurement.temperature)+", "+str(measurement.humidity)+" ,"+ str(measurement.battery))
    file.write(os.linesep)
    file.close()
# Main loop --------

#Medida ()

