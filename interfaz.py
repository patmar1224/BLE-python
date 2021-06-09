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
        #CONECTAR SENSOR
        self.ui.boton_conectar_sensor.clicked.connect(self.funcion_conectar_sensor)
        self.ui.mensaje_mac.textChanged.connect(lambda: self.ui.mensaje_mac.setStyleSheet("QLineEdit { color: white}"))
        #MENU
        self.ui.boton_sensor1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_1))
        self.ui.boton_sensor2.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor2_1))
        self.ui.boton1_1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_1))
        self.ui.boton1_2.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_2))
        self.ui.boton1_3.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_3))
        self.ui.boton2_1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor2_1))
        self.ui.botonInicio.clicked.connect (lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.home))
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
        self.ui.boton_on.clicked.connect(self.funcion_encender) 
        self.ui.boton_off.clicked.connect(self.funcion_apagar)
        self.ui.boton_brillo.clicked.connect(self.funcion_brillo)
        self.ui.mensaje_brillo.textChanged.connect(lambda: self.ui.mensaje_brillo.setStyleSheet("QLineEdit { color: white}"))
        
        
    def funcion_buscar(self):
        print('Pulsado')
        self.ui.nueva_ventana.exec()
        
    def funcion_conectar_sensor(self):
        global mac
        global valido
        mac=str(self.ui.direccion_MAC.toPlainText())
        print(mac)
        if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$",mac):
            print ("MAC correcta")
            self.ui.mensaje_mac.setText("MAC válida")
            valido=True
            connect(mac)
        else:
            print ("Introduce la MAC en formato AA:BB:CC:DD:EE:FF sin importar las mayusculas")
            self.ui.mensaje_mac.setText("Error, MAC en formato AA:BB:CC:DD:EE:FF")
            valido=False

    #Para el boton tomar medida     
    def funcion_medida(self):
        if valido==False:
            self.ui.mensaje_mac.setText("No se puede realizar medidas MAC no valida")
            print("No se puede realizar medidas, MAC no valida")
        else:    
            Medida(mac)
            self.ui.Temperatura.setText(str(measurement.temperature))
            self.ui.Humedad.setText(str(measurement.humidity))
            self.ui.Bateria.setText(str(measurement.battery))
            self.ui.Voltaje.setText(str(measurement.voltage))
            #Guardar los datos
            self.ui.datos=[]
            self.ui.datos.append((datetime.today().strftime('%d-%m-%Y'),time.strftime("%H:%M:%S"),str(measurement.temperature),str(measurement.humidity),str(measurement.battery)))
            date=float(time.strftime("%H.%M")) #Para meterlo en la gráfica
            temp=measurement.temperature
            hum=measurement.humidity
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
    #Funciones de bombilla.py
    def conectar_sensor (self):
        global valido_luz
        
    def funcion_encender (self):
        encender()
    def funcion_apagar (self):
        apagar()
    def funcion_brillo(self):
        if not self.ui.textEdit.toPlainText() or self.ui.textEdit.toPlainText().isdigit() == False or float(self.ui.textEdit.toPlainText())== True:
            self.ui.mensaje_brillo.setText("Número no válido. Rango entre 1 y 254")
            #print(self.ui.textEdit.toPlainText())
            if int(self.ui.textEdit.toPlainText())==1:
                self.ui.mensaje_brillo.setText("Número válido")
                brillo(1)
        else:
            bri=int(self.ui.textEdit.toPlainText())
            #print (bri)
            if bri>0 and bri<255:
                self.ui.mensaje_brillo.setText("Número válido")
                brillo(bri)
            else: 
                self.ui.mensaje_brillo.setText("Número no válido. Rango entre 1 y 254")
        
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
        
if __name__ == '__main__':
    app=QApplication(sys.argv) #Para abrir la aplicación
    GUI = ejemplo_GUI()
    nueva_ventana=Nueva_ventana()
    GUI.show()
    valido=False
    valido_luz=False
    sys.exit(app.exec_())
        