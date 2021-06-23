import sys
from PyQt5 import uic #Carga la aplicación del Qt designer
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem #Para cargar la aplicación
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
from SensorLYWSD03MMC import *
from bombilla import *
from datetime import datetime
import time
import datetime
from gui_app import Ui_MainWindow
from busqueda import funcion_busqueda
import re
from cayenne import *
import numpy as np
import matplotlib.dates as mdates

class ejemplo_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        #uic.loadUi ("gui_app.ui", self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_1)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_2)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_3)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_4)
        self.ui.stackedWidget.setCurrentWidget(self.ui.sensor2_1)
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        #BOTONES LÍNEA SUPERIOR
        self.ui.boton_minimizar.clicked.connect(lambda:self.showMinimized())
        self.ui.boton_cerrar.clicked.connect(lambda:self.close())
        #LISTAR DISPOSITIVOS EN NUEVA VENTANA
        self.ui.boton_buscar.clicked.connect(self.funcion_buscar)
        self.ui.nueva_ventana = Nueva_ventana()
        #EMPAREJAR SENSOR NUEVA VENTANA
        self.ui.boton_emparejar.clicked.connect(self.funcion_emparejar)
        self.ui.emparejar_ventana = Emparejar_ventana()
        self.ui.mensaje_emparejar.textChanged.connect(lambda: self.ui.mensaje_emparejar.setStyleSheet("QLineEdit { color: white}"))
        self.ui.mensaje_sensor.textChanged.connect(lambda: self.ui.mensaje_sensor.setStyleSheet("QLineEdit { color: white}"))
        #EMPAREJAR BOMBILLA NUEVA VENTANA
        self.ui.boton_emparejar_bombilla.clicked.connect(self.funcion_emparejar_bombilla)
        self.ui.emparejar_ventanaBombilla = Emparejar_ventanaBombilla()
        self.ui.mensaje_emparejar_bombilla.textChanged.connect(lambda: self.ui.mensaje_emparejar_bombilla.setStyleSheet("QLineEdit { color: white}"))
        self.ui.mensaje_bombilla.textChanged.connect(lambda: self.ui.mensaje_bombilla.setStyleSheet("QLineEdit { color: white}"))
        #MENU
        self.ui.boton_sensor1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_1))
        self.ui.boton_sensor2.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor2_1))
        self.ui.boton1_1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_1))
        self.ui.boton1_2.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_2))
        self.ui.boton1_3.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_3))
        self.ui.boton1_4.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor1_4))
        self.ui.boton2_1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor2_1))
        self.ui.botonInicio.clicked.connect (lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.home))
        self.ui.boton_auto.clicked.connect (lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.Pagina_Auto))
        #SENSOR XIAOMI DATOS ACTUALES
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
        #SENSOR XIAOMI GRÁFICA
        self.figura=self.ui.grafica.canvas.fig
        self.ejes1=self.figura.add_subplot(211)
        self.ejes2=self.figura.add_subplot(212)
        #xlim = [0.0, 23.59]
        x = ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00","14:00", "16:00", "18:00", "20:00", "22:00", "23:59"]
        dates_graf = [datetime.datetime.strptime(h, "%H:%M") for h in x]
        xformater = mdates.DateFormatter('%H:%M')
        ylim = [0, 60]
        ylim2=[0, 100]
        #self.ejes1.set_xlim(xlim)
        self.ejes1.xaxis.set_major_formatter(xformater)
        self.ejes1.set_xlim((min(dates_graf) - datetime.timedelta(hours=1),max(dates_graf) + datetime.timedelta(hours=1)))
        self.ejes1.set_ylim(ylim)
        #self.ejes2.set_xlim(xlim)
        self.ejes2.xaxis.set_major_formatter(xformater)
        self.ejes2.set_xlim((min(dates_graf) - datetime.timedelta(hours=1),max(dates_graf) + datetime.timedelta(hours=1)))
        self.ejes2.set_ylim(ylim2)
        self.ejes1.set(ylabel='Temperatura (ºC)', title='Temperatura y Humedad')
        self.ejes2.set(xlabel='Tiempo (h)', ylabel='Humedad (%)')
        self.ejes1.grid()
        self.ejes2.grid()
        #SENSOR XIAOMI CARGAR DATOS
        self.ui.boton_CargarDatos.clicked.connect(self.funcion_CargarDatosEnTabla)
        self.ui.boton_BorrarDatos.clicked.connect(self.funcion_BorrarDatos)
        self.ui.boton_VisualizarDatos.clicked.connect(self.funcion_VisualizarDatos)
        #BOMBILLA
        self.ui.boton_on.clicked.connect(self.funcion_encender) 
        self.ui.boton_off.clicked.connect(self.funcion_apagar)
        self.ui.boton_brillo.clicked.connect(self.funcion_brillo)
        self.ui.mensaje_brillo.textChanged.connect(lambda: self.ui.mensaje_brillo.setStyleSheet("QLineEdit { color: white}"))
        #MODO AUTOMÁTICO-ESCENAS
        self.ui.modoAuto.stateChanged.connect(self.funcion_ModoAuto)
        self.ui.spinBox_brillo.editingFinished.connect(self.funcion_ModoAuto)
        self.ui.spinBox_humedad.editingFinished.connect(self.funcion_ModoAuto)
        
    #FUNCIÓN BOTÓN LISTAR DISPOSTIVOS    
    def funcion_buscar(self):
        print('Pulsado')
        self.ui.nueva_ventana.exec()
        
    #EMPAREJAR SENSOR   
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
            
    #EMPAREJAR BOMBILLA
    def funcion_emparejar_bombilla(self):
        self.ui.emparejar_ventanaBombilla.exec()
        
    def funcion_texto_inicio_bombilla(self):
        if valido_bombilla == True:
            self.ui.mensaje_emparejar_bombilla.setText("Sensor "+ str(mac_bombilla) + " emparejado")
            self.ui.mensaje_bombilla.setText("Sensor "+ str(mac_bombilla) + " emparejado")
        else:
            self.ui.mensaje_emparejar_bombilla.setText("Ningún sensor emparejado")
            self.ui.mensaje_bombilla.setText("Ningún sensor emparejado")
            
    #FUNCIONES SENSOR     
    def funcion_medida(self):
        global cont
        global date_anterior
        global temp_anterior
        global hum_anterior
        global dia_anterior
        
        if valido_sensor==False:
            self.ui.mensaje_sensor.setText("No se pueden hacer medidas no emparejado")
            print("No se puede realizar medidas, sensor no emparejdo")
        else:    
            Medida(mac)
            #date=float(time.strftime("%H.%M")) #Para meterlo en la gráfica
            dia=datetime.datetime.today().strftime('%d') #valor de día 
            temp=measurement.temperature
            hum=measurement.humidity
            bat= measurement.battery
            vol=measurement.voltage
            self.ui.Temperatura.setText(str(temp))
            self.ui.Humedad.setText(str(hum))
            self.ui.Bateria.setText(str(bat))
            self.ui.Voltaje.setText(str(vol))
            #Guardar los datos
            datos=[]
            datos.append((datetime.datetime.today().strftime('%d-%m-%Y'),time.strftime("%H:%M:%S"),str(temp),str(hum),str(bat)))
            print(datos)
            #Agregar contenido a la tabla
            fila=0
            for registro in datos:
                columna=0
                self.ui.tabla_sensor.insertRow(fila)
                for elemento in registro:                
                    celda=QTableWidgetItem(elemento)
                    self.ui.tabla_sensor.setItem(fila,columna,celda)
                    columna+=1
                fila+=1
           #La gráfica se reinicia cuando el día ya es diferente
            if dia_anterior!=dia:
                self.figura=self.ui.grafica.canvas.fig
                self.ejes1=self.figura.add_subplot(211)
                self.ejes2=self.figura.add_subplot(212)
                x = ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00","14:00", "16:00", "18:00", "20:00", "22:00", "23:59"]
                dates_graf = [datetime.datetime.strptime(h, "%H:%M") for h in x]
                xformater = mdates.DateFormatter('%H:%M')
                ylim = [0, 60]
                ylim2=[0, 100]
                self.ejes1.xaxis.set_major_formatter(xformater)
                self.ejes1.set_xlim((min(dates_graf) - datetime.timedelta(hours=1),max(dates_graf) + datetime.timedelta(hours=1)))
                self.ejes1.set_ylim(ylim)
                self.ejes2.xaxis.set_major_formatter(xformater)
                self.ejes2.set_xlim((min(dates_graf) - datetime.timedelta(hours=1),max(dates_graf) + datetime.timedelta(hours=1)))
                self.ejes2.set_ylim(ylim2)
                self.ejes1.set(ylabel='Temperatura (ºC)', title='Temperatura y Humedad')
                self.ejes2.set(xlabel='Tiempo (h)', ylabel='Humedad (%)')
                self.ejes1.grid()
                self.ejes2.grid()
                self.ui.grafica.canvas.draw()
                cont=0
                
            pr = [(datetime.datetime.now().strftime("%H:%M"))]
            x = [datetime.datetime.strptime(h, "%H:%M") for h in pr]
            
            if cont == 0:
                self.ejes1.scatter(x, temp)
                self.ejes2.scatter(x, hum, marker='s')
            else:
                self.ejes1.scatter(x, temp)
                self.ejes2.scatter(x, hum, marker='s')
                self.ejes1.errorbar([date_anterior,x],[temp_anterior,temp])
                self.ejes2.errorbar([date_anterior,x],[hum_anterior,hum])
                print (date_anterior)
            
          
                
            date_anterior=x
            temp_anterior=temp
            hum_anterior=hum
            dia_anterior=dia
            cont=1
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
                    
            #funcion_guardar_datos_tabla(self)
   
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
    
    #Para modificar los datos cargados
    def funcion_BorrarDatos(self):
        open("/home/pi/BLE-python/Cargar_Datos_Antiguos.txt", "w").close()
        with open('Cargar_Datos_Antiguos.txt', 'r') as myfile:
            datos_fichero=myfile.read()
        self.ui.Listar_Datos.setText(str(datos_fichero))
        
    def funcion_VisualizarDatos(self):
         with open('Cargar_Datos_Antiguos.txt', 'r') as myfile:
            datos_fichero=myfile.read()
         self.ui.Listar_Datos.setText(str(datos_fichero))
    
    def funcion_CargarDatosEnTabla (self):
        datos_anteriores=np.loadtxt("/home/pi/BLE-python/Cargar_Datos_Antiguos.txt", delimiter=os.linesep, dtype="str")
        print(datos_anteriores)
        #porque con una sola medida da errores
        l=[]
        l.append(str(datos_anteriores))
        if datos_anteriores.size==1:
            datos_anteriores=l
        #meter los datos en la tabla
        fila=0
        for registro in reversed(datos_anteriores):
             columna=0
             self.ui.tabla_sensor.insertRow(fila)
             for elemento in registro.split(" | "):                
                 celda=QTableWidgetItem(elemento)
                 self.ui.tabla_sensor.setItem(fila,columna,celda)
                 columna+=1
             fila+=1
        
    #BOMBILLA      
    def funcion_encender (self):
        if valido_bombilla==True:
            encender()
            enviar_bombilla_nube(254)
        
    def funcion_apagar (self):
        if valido_bombilla==True:
            apagar()
            enviar_bombilla_nube(0)
        
    def funcion_brillo(self):
        if valido_bombilla==True:
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
    
    #MODO AUTOMÁTICO            
    def funcion_ModoAuto(self):
        global MedidaAutomatica
        if self.ui.modoAuto.isChecked()==True:
            MedidaAutomatica=True
        else:
            MedidaAutomatica=False
            
#VENTANAS EXTERNAS
#Ventana de búsqueda de dispositivos Bluetooth
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
        
#Ventana de emparejar el sensor  
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
              #Si introduces mal la mac mira si la del fichero es correcta y se queda con esa
            with open('Guardar_mac_sensor.txt', 'r') as myfile:
                mac=myfile.read()
            if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$",mac_bombilla):
                valido_sensor=True
                self.mensaje_mac.setText("Mac no válida, sensor " + str(mac) + " anterior emparejado")

            else:
                valido_sensor=False
            
        GUI.funcion_texto_inicio()
            
#Ventana de emparejar la bombilla          
class Emparejar_ventanaBombilla (QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ventana_emparejar_bombilla.ui", self)
        self.emparejar_bombilla.clicked.connect(self.funcion_emparejando)
        self.mensaje_mac.textChanged.connect(lambda: self.mensaje_mac.setStyleSheet("QLineEdit { color: white}"))
        
    def funcion_emparejando (self):
        global mac_bombilla
        global valido_bombilla
        mac_bombilla=str(self.direccion_mac_bombilla.toPlainText())
        print(mac_bombilla)
        if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$",mac_bombilla):
            print ("MAC correcta")
            self.mensaje_mac.setText("MAC válida")
            valido_bombilla=True
            GUI.funcion_texto_inicio_bombilla()
            configuracion_bombilla(str(mac_bombilla))
            file=open("/home/pi/BLE-python/Guardar_mac_bombilla.txt", "w")
            file.write(str(mac_bombilla))
            file.close()
            
        else:
            print ("Introduce la MAC en formato AA:BB:CC:DD:EE:FF sin importar las mayusculas")
            self.mensaje_mac.setText("Error, MAC en formato AA:BB:CC:DD:EE:FF")
            #Si introduces mal la mac mira si la del fichero es correcta y se queda con esa
            with open('Guardar_mac_bombilla.txt', 'r') as myfile:
                mac_bombilla=myfile.read()
            if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$",mac_bombilla):
                valido_bombilla=True
                self.mensaje_mac.setText("Mac no válida, sensor " + str(mac_bombilla) + " anterior emparejado")

            else:
                valido_bombilla=False
         
        GUI.funcion_texto_inicio_bombilla()
            
#MAIN           
if __name__ == '__main__':
    app=QApplication(sys.argv) #Para abrir la aplicación
    GUI = ejemplo_GUI()
    nueva_ventana=Nueva_ventana()
    emparejar_ventana=Emparejar_ventana()
    emparejar_ventanaBombilla=Emparejar_ventanaBombilla()
    GUI.show()
    #Comprobar si el sensor está guardado
    with open('Guardar_mac_sensor.txt', 'r') as myfile:
        mac=myfile.read()
    if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$",mac):
        valido_sensor=True
    else:
        valido_sensor=False
        
    #Comprobar que la bombilla está guardada   
    with open('Guardar_mac_bombilla.txt', 'r') as myfile:
        mac_bombilla=myfile.read()
    if re.match("[0-9a-fA-F]{2}([:]?)[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$",mac_bombilla):
        valido_bombilla=True
        configuracion_bombilla(str(mac_bombilla))
    else:
        valido_bombilla=False
        
    GUI.funcion_texto_inicio()
    GUI.funcion_texto_inicio_bombilla()
    
    #Meter los datos actuales en el fichero de los datos antiguos antes de borrarlo
    file=open("/home/pi/BLE-python/Cargar_Datos_Antiguos.txt", "a")
    with open('Datos_sensor.txt', 'r') as myfile:
         datos_fichero=myfile.read()      
    file.write(datos_fichero)
    file.close()
    open("/home/pi/BLE-python/Datos_sensor.txt", "w").close() #Para borrar los datos del sensor y empezar de nuevo
    
    MedidaAutomatica=False
    
    #Para pintar la gráfica uniendo sus puntos
    cont=0
    date_anterior=0
    temp_anterior=0
    hum_anterior=0
    dia_anterior=datetime.datetime.today().strftime('%d')
   
    app.exec_()
    #sys.exit()
        