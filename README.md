# Zigbee-python
Conexión del sensor Xiaomi Aqara Multi sensor WSDCGQ11LM (sensor de temperatura, humedad y presión atmosférica) y bombilla IKEA TRÅDFRI 470 lm E14 (bombilla con luz de colores, luz cálida y fría). Esta conexión se realizará en lenguaje Python y además se utilizará un USB universal Zigbee gateway, ConBee 2.

# Como instalar conbee II (deconz) en la raspberry pi
-Primero se deben de establecer los derechos de acceso USB del usuario:
sudo gpasswd -a $USER dialout

-Importar clave pública de Phoscon (web de Conbee II)
wget -O - http://phoscon.de/apt/deconz.pub.key | \

-Tras el anterior comando la consola espera que introduzcas el siguiente comando:
sudo apt-key add -

-Configurar el repositorio APT para deCONZ:
sudo sh -c "echo 'deb http://phoscon.de/apt/deconz \
$(lsb_release -cs) main' > \
/etc/apt/sources.list.d/deconz.list"

-A continuación se va a actualizar la raspberry:
sudo apt update

-Instalación de deconz:
sudo apt install deconz

-Preguntará si quieremos continuar, diremos que sí introduciendo una Y y presionando intro.

-Comprobar si tenemos activo el sistema que acabamos de instalar lanzando el siguiente comando:
systemctl status deconz

-En caso de que el sistema esté INACTIVE, pulsamos Control + C, y restablecemos el funcionamiento del sistema con el siguiente comando:
sudo service deconz start

-Volvemos a comprobar el estado para ver que ahora es ACTIVE:
systemctl status deconz

-La siguiente linea sirve para que deconz se inicie siempre que arranque la raspberry, no es obligatorio pero si recomendable:
sudo systemctl enable deconz

-En el caso, de que no pongamos el anterior comando, deberemos de comprobar el estado del deconz cada vez que se inicie la raspberry y en caso de que este INACTIVE, restableceremos el sistema como hemos hecho anteriormente:
sudo service deconz start

-Una vez se han introducido todos los comandos se debe de hacer un reinicio de la raspberry para que se apliquen los cambios.

En caso de duda consultar la siguiente página:
https://accounts.mydevices.com/auth/realms/cayenne/protocol/openid-connect/auth?response_type=code&scope=email+profile&client_id=cayenne-web-app&state=5Os6WlKS3imyU0xcCTtRBT4CiLtndkUf2O7QUpFo&redirect_uri=https%3A%2F%2Fcayenne.mydevices.com%2Fauth%2Fcallback

# Para el buen funcionamiento de la app
Se deberá de añadir la IP de nuestra raspberry en los ficheros deconz_aqara_multisensor.py y bombilla_ikea.py

# Poner en marcha la APP
La aplicación se ha desarrollado con QtDesigner. Para instalar el entorno gráfico debemos introducir los siguientes comandos:
sudo apt-get install python-pyqt5 
sudo apt-get install qtcreator pyqt5-dev-tools 
sudo apt-get install python3-pyqt5 
sudo apt-get install pttools5-dev-tools 
pip install pyinstaller 

#MyDevice cayenne
MyDevice.com es una plataforma dondese subiran los datos de nuestra app en la nube, a la vez que podremos controlar el sensor y la bombilla desde ahí. Primero nos debemos de crear una cuenta en myDevices.com y desde ahí seguir todos los pasos. El URL de la página es el siguiente:
https://accounts.mydevices.com/auth/realms/cayenne/protocol/openid-connect/auth?response_type=code&scope=email+profile&client_id=cayenne-web-app&state=5Os6WlKS3imyU0xcCTtRBT4CiLtndkUf2O7QUpFo&redirect_uri=https%3A%2F%2Fcayenne.mydevices.com%2Fauth%2Fcallback




