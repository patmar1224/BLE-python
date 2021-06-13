#Prueba de la nube -> myDevices.com
#Librerias
import paho.mqtt.client as mqtt
import time
from bombilla import *

#Información sacada diredctamente de la plataforma myDevices
user = 'f9214a20-cb76-11eb-883c-638d8ce4c23d'
password = 'f7c6a360cadab1e25467ef8471c738f7da6c6c4a'
client_id = '47b56be0-cb7b-11eb-b767-3f1a8f1211ba'
server = 'mqtt.mydevices.com'
port = 1883

publish_0 = 'v1/' + user + '/things/' + client_id + '/data/0' #Valor temperatura
publish_1 = 'v1/' + user + '/things/' + client_id + '/data/1' #Valor de humedad
publish_2 = 'v1/' + user + '/things/' + client_id + '/data/2' #Valor de la batería

publish_4 = 'v1/' + user + '/things/' + client_id + '/data/4' #Estado de la bombilla 1 encendido 0 apagado
publish_encender = 'v1/' + user + '/things/' + client_id + '/data/3' #Para el boton de encender la bombilla
subscribe_encender = 'v1/' + user + '/things/' + client_id + '/cmd/3'

def enviar_temp_nube(t):
    client.publish(publish_0,t)

def enviar_hum_nube(h):
    client.publish(publish_1, h)

def enviar_bat_nube(b):
    client.publish(publish_2, b)
def enviar_bombilla_nube (b):
     client.publish(publish_4, b)

def mensagens(client, userdata, msg): 
     m = msg.topic.split('/')
     p = msg.payload.decode().split(',')
     print(m)
     print(p)
     client.publish(publish_encender, p[1])
     #print(p[1])
     if p[1]== '0':
         apagar()
         client.publish(publish_4, 0)
     else:
         encender()
         brillo(int(p[1]))
         client.publish(publish_4, int(p[1]))

client = mqtt.Client(client_id)
client.username_pw_set(user, password)
client.connect(server, port)
client.on_message = mensagens 
client.subscribe(subscribe_encender)

client.loop_start()
# 
# for i in range(1, 10):
#      client.publish(publish_0,i)
#      client.publish(publish_1,i*2.1)
#      time.sleep(2)
