import sys
from PyQt5 import uic #Carga la aplicación del Qt designer
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem #Para cargar la aplicación
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
import qtawesome as qta
from SensorLYWSD03MMC import *
from SensorLYWSD03MMC import measurement
from datetime import datetime
import time
from gui_app import Ui_MainWindow
from busqueda import funcion_busqueda
import re
from bombilla import *
from cayenne import *

class ejemplo_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        #uic.loadUi ("gui_app.ui", self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_1)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_2)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_2)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor2_1)
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        #LISTAR DISPOSITIVOS EN NUEVA VENTANA
        self.ui.boton_buscar.clicked.connect(self.funcion_buscar)
        self.ui.nueva_ventana = Nueva_ventana()
        #BOTONES LÍNEA SUPERIOR
        self.ui.boton_minimizar.clicked.connect(lambda:self.showMinimized())
        self.ui.boton_cerrar.clicked.connect(lambda:self.close())
        #EMPAREJAR SENSOR
        self.ui.boton_emparejar.clicked.connect(self.funcion_emparejar)
        self.ui.emparejar_ventana = Emparejar_ventana()
        self.ui.mensaje_emparejar.textChanged.connect(lambda: self.ui.mensaje_emparejar.setStyleSheet("QLineEdit { color: white}"))
        self.ui.mensaje_sensor.textChanged.connect(lambda: self.ui.mensaje_sensor.setStyleSheet("QLineEdit { color: white}"))
        #MENU
        self.ui.boton_sensor1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_1))
        self.ui.boton_sensor2.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor2_1))
        self.ui.boton1_1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_1))
        self.ui.boton1_2.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_2))
        self.ui.boton1_3.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_3))
        self.ui.boton2_1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor2_1))
        self.ui.botonInicio.clicked.connect (lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.home))
        self.ui.boton_auto.clicked.connect (lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.Pagina_Auto))
        #BOTONES DEL SENSOR XIAOMI DATOS ACTUALES
        self.ui.botonMedida.clicked.connect (self.funcion_medida)
        self.ui.medidaautomatica.stateChanged.connect(self.funcion_MedidaAuto)
        self.ui.spinBox.editingFinished.connect(self.funcion_MedidaAuto)
        #Creación del timer
        self.ui.timer=QTimer()
        self.ui.timer.timeout.connect(self.funcion_medida)
        #SENSOR XIAOMI TABLA
        #Ajustar la tabla al tamaño 
        #self.tabla_sensor.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        #self.tabla_sensor.resizeColumnsToContents() 
        #Modificar elementos tabla
        self.ui.boton_borrartabla_entera.clicked.connect (self.funcion_borrartabla)
        self.ui.boton_borrartabla_ultimo.clicked.connect(self.funcion_borrartabla_ultimo)
        #GRAFICA
        self.figura=self.ui.grafica.canvas.fig
        self.ejes1=self.figura.add_subplot(211)
        self.ejes2=self.figura.add_subplot(212)
        xlim = [0.0, 23.59]
        ylim = [0, 60]
        ylim2=[0, 100]
        self.ejes1.set_xlim(xlim)
        self.ejes1.set_ylim(ylim)
        self.ejes2.set_xlim(xlim)
        self.ejes2.set_ylim(ylim2)
        self.ejes1.set(ylabel='Temperatura (ºC)', title='Temperatura y Humedad')
        self.ejes2.set(xlabel='Tiempo (h)', ylabel='Humedad (%)')
        self.ejes1.grid()
        self.ejes2.grid()
        #BOMBILLA
        self.ui.boton_on.clicked.connect(self.funcion_encender) 
        self.ui.boton_off.clicked.connect(self.funcion_apagar)
        self.ui.boton_brillo.clicked.connect(self.funcion_brillo)
        self.ui.mensaje_brillo.textChanged.connect(lambda: self.ui.mensaje_brillo.setStyleSheet("QLineEdit { color: white}"))
        #Modo Automatico
        self.ui.modoAuto.stateChanged.connect(self.funcion_ModoAuto)
        self.ui.spinBox_brillo.editingFinished.connect(self.funcion_ModoAuto)
        self.ui.spinBox_humedad.editingFinished.connect(self.funcion_ModoAuto)
        
        
    def funcion_buscar(self):
        print('Pulsado')
        self.ui.nueva_ventana.exec()
        
    #EMPAREJAR    
    def funcion_emparejar(self):
        print ('Emperajando')
        self.ui.emparejar_ventana.exec()
        
    def funcion_texto_inicio(self):
        if valido_sensor == True:
            self.ui.mensaje_emparejar.setText("Sensor "+ str(mac) + " emparejado")
            self.ui.mensaje_sensor.setText("Sensor "+ str(mac) + " emparejado")
        else:
            self.ui.mensaje_emparejar.setText("Ningún sensor emparejado")
            self.ui.mensaje_sensor.setText("Ningún sensor emparejado")
            
    #FUNCIONES SENSOR     
    def funcion_medida(self):
        if valido_sensor==False:
            self.ui.mensaje_sensor.setText("No se pueden hacer medidas no emparejado")
            print("No se puede realizar medidas, sensor no emparejdo")
        else:    
            Medida(mac)
            date=float(time.strftime("%H.%M")) #Para meterlo en la gráfica
            temp=measurement.temperature
            hum=measurement.humidity
            bat= measurement.battery
            vol=measurement.voltage
            self.ui.Temperatura.setText(str(temp))
            self.ui.Humedad.setText(str(hum))
            self.ui.Bateria.setText(str(bat))
            self.ui.Voltaje.setText(str(vol))
            #Guardar los datos
            self.ui.datos=[]
            self.ui.datos.append((datetime.today().strftime('%d-%m-%Y'),time.strftime("%H:%M:%S"),str(temp),str(hum),str(bat)))
            
            #Agregar contenido a la tabla
            fila=0
            for registro in self.ui.datos:
                columna=0
                self.ui.tabla_sensor.insertRow(fila)
                for elemento in registro:                
                    celda=QTableWidgetItem(elemento)
                    self.ui.tabla_sensor.setItem(fila,columna,celda)
                    columna+=1
                fila+=1
            #self.ejes1.scatter(date, temp, color='green')
            self.ejes1.scatter(date, temp)
            self.ejes2.scatter(date, hum, marker='s')
            #self.ejes.errorbar([date_anterior,date],[temp_anterior, temp])
            #date_anterior=date
            #temp_anterior=temp  
            self.ui.grafica.canvas.draw()
            enviar_temp_nube(temp)
            enviar_hum_nube(hum)
            enviar_bat_nube(bat)
            if MedidaAutomatica == True:
                if self.ui.spinBox_humedad.value() == hum:
                    encender()
                    brillo (self.ui.spinBox_brillo.value())
                    enviar_bombilla_nube(self.ui.spinBox_brillo.value())
                else:
                    apagar()
                    enviar_bombilla_nube(0)
   
    def funcion_MedidaAuto(self):
        if self.ui.medidaautomatica.isChecked()==True:
            #print(self.spinBox.value())
            self.ui.timer.start(self.ui.spinBox.value()*60000) #60000 porque quiero minutos y se guarda en ms
        else:
            self.ui.timer.stop()
            
    #Para modificar la tabla       
    def funcion_borrartabla(self):
        self.ui.tabla_sensor.clearContents()
        fila=self.ui.tabla_sensor.rowCount()
        for fila in range (-1, self.ui.tabla_sensor.rowCount()):
            self.ui.tabla_sensor.removeRow(fila)
            self.ui.tabla_sensor.removeRow(0)
            fila-=1
            
    def funcion_borrartabla_ultimo(self):
        self.ui.tabla_sensor.removeRow(1)
        
    #BOMBILLA
    def conectar_sensor (self):
        global valido_luz
        
    def funcion_encender (self):
        encender()
        enviar_bombilla_nube(254)
        
    def funcion_apagar (self):
        apagar()
        enviar_bombilla_nube(0)
        
    def funcion_brillo(self):
        if not self.ui.textEdit.toPlainText() or self.ui.textEdit.toPlainText().isdigit() == False or float(self.ui.textEdit.toPlainText())== True:
            self.ui.mensaje_brillo.setText("Número no válido. Rango entre 1 y 254")
            #print(self.ui.textEdit.toPlainText())
            if int(self.ui.textEdit.toPlainText())==1:
                self.ui.mensaje_brillo.setText("Número válido")
                brillo(1)
                enviar_bombilla_nube(1)
        else:
            bri=int(self.ui.textEdit.toPlainText())
            #print (bri)
            if bri>0 and bri<255:
                self.ui.mensaje_brillo.setText("Número válido")
                brillo(bri)
                enviar_bombilla_nube(bri)
            else: 
                self.ui.mensaje_brillo.setText("Número no válido. Rango entre 1 y 254")
                
    def funcion_ModoAuto(self):
        global MedidaAutomatica
        if self.ui.modoAuto.isChecked()==True:
            MedidaAutomatica=True
        else:
            MedidaAutomatica=False
            
#VENTANAS EXTERNAS       
class Nueva_ventana (QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("segunda_ventana.ui", self)
        self.boton_comenzar_busqueda.clicked.connect(self.funcion_comenzar_busqueda)
    def funcion_comenzar_busqueda(self):
        funcion_busqueda()
        with open('dispositivos.txt', 'r') as myfile:
            data=myfile.read()
        self.texto.setText(str(data))
    
class Emparejar_ventana (QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ventana_emparejar.ui", self)
        self.emparejar.clicked.connect(self.funcion_emparejando)
        self.mensaje_mac.textChanged.connect(lambda: self.mensaje_mac.setStyleSheet("QLineEdit { color: white}"))
    def funcion_emparejando (self):
        global mac
        global valido_sensor
        mac=str(self.direccion_MAC.toPlainText())
        print(mac)
        if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$",mac):
            print ("MAC correcta")
            self.mensaje_mac.setText("MAC válida")
            valido_sensor=True
            GUI.funcion_texto_inicio()
            connect(mac)
            file=open("/home/pi/BLE-python/Guardar_mac_sensor.txt", "w")
            file.write(str(mac))
            file.close()
            
        else:
            print ("Introduce la MAC en formato AA:BB:CC:DD:EE:FF sin importar las mayusculas")
            self.mensaje_mac.setText("Error, MAC en formato AA:BB:CC:DD:EE:FF")
            valido_sensor=False 
        
if __name__ == '__main__':
    app=QApplication(sys.argv) #Para abrir la aplicación
    GUI = ejemplo_GUI()
    nueva_ventana=Nueva_ventana()
    emparejar_ventana=Emparejar_ventana()
    GUI.show()
    with open('Guardar_mac_sensor.txt', 'r') as myfile:
        mac=myfile.read()
    if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$",mac):
        valido_sensor=True
        #self.ui.mensaje_emparejar.setText("Sensor emparejado")
    else:
        valido_sensor=False
    GUI.funcion_texto_inicio()  
    valido_luz=False
    MedidaAutomatica=False
    app.exec_()
    #sys.exit()
        