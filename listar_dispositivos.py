#-*- coding: utf-8 -*-
from bluepy.btle import Scanner, DefaultDelegate
import os
cont=0
global file

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
            #file.write("Discovered device "+str(dev.addr))
            #file.write(os.linesep)
        elif isNewData:
            print ("Received new data from", dev.addr)
            #file.write("Received new data from "+str(dev.addr))
            #file.write(os.linesep)
            
def listar_dispositivos():
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)
    for dev in devices:
        print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        file.write("·Device "+ str(dev.addr) + str(dev.addrType) + ", RSSI= "+ str(dev.rssi) + "dB")
        file.write(os.linesep)
        for (adtype, desc, value) in dev.getScanData():
            print ("  %s = %s" % (desc, value))
            file.write( str(desc) + str(value) )
            file.write(os.linesep)
    file.close()
 
open("/home/pi/BLE-python/dispositivos.txt", "w").close() #para borrarlo cada vez que se abra 
file=open("/home/pi/BLE-python/dispositivos.txt", "a") 
listar_dispositivos()