 # BLE-python
Conexión de dispositivos BLE, bombilla Philips Hue (luz blanca y brillo ajustable) y sensor xiaomi Mijia (sensor de temperatura y humedad).
Para el funcionamiento de este proyecto se necesitan los siguietnes requisitos:

-Pyhton instalado superior a 3.7

-Sistema operativo linux

-Raspberry pi 4 (o Raspberry inferior con adaptador bluetooth dotado con BLE)

# Para el sensor de temperatura y humedad
-Instalación de bluez:

	 sudo apt install python3 bluez python3-pip
	 pip3 install pybluez
	 pip3 install bluepy

# Para el entorno gráfico de la aplicación:
-Necesario tener instalado pyqt5 y Qt Designer

	-sudo apt-get install python-pyqt5
	-sudo apt-get install qtcreator pyqt5-dev-tools
	-sudo apt-get install python3-pyqt5
	-sudo apt-get install pttools5-dev-tools
	-pip install pyinstaller 
	-sudo apt-get install pyton3-qtawesome (librería para iconos)

# Para la bombilla

	-pip3 install pydbus
	-Versión de Bluetooth igual o superior a 5.50 (se comprueba con el comando bluetoothctl -v)
	-Emparejar la bombilla con el bluetooth de la Raspberry pi

# Para la subida de datos a la nube Cayenne: 
-Necesario tener una cuenta en la página web de cayenne para la subida de resultados, en el siguiente enlace: https://accounts.mydevices.com/auth/realms/cayenne/protocol/openid-connect/auth?response_type=code&scope=email+profile&client_id=cayenne-web-app&state=Ni9R7ZJ0NLdEJUuYqcbTxfOu1ndxWF6QxvMmEXcp&redirect_uri=https%3A%2F%2Fcayenne.mydevices.com%2Fauth%2Fcallback

-Seguir los pasos que se indican una vez te creas la cuenta para instalar cayenne en la raspberry

-Cambiar los datos de usurio, contraseña, cliente, servidor y puerto del fichero cayenne.py por los datos que te muestra después de crearte la cuenta 

-Crear un nuevo proyecto con el nombre cayenne, añadir temperatura, humedad y batería para actualizar los datos

# Para la subida de datos a la nube Dropbox:
-Instalar la libreria de dropbox: pip install dropbox

-Cuenta en Dropbox y creación de la app en el siguiente enlace:https://www.dropbox.com/developers

-Dar todos los permisos de lectura y escritura a la aplicación:
	-En el apartado Permissions activar todos los de Individual Scopes

-Generar el token:
	-En el apartado OAuth 2 en el botón Generate

-Una vez este lista la aplicación se crea un fichero en esta carpeta de dropbox, con el mismo nombre y extensión cuyo nombre de fichero se quiere subir.

# Para la subida de datos a la nube Kaaiot:
-pip install paho-mqtt

-Cuenta en Kaaiot

-Conectar la raspberry en tu nube de kaaiot mediante la opción add devices

-Al agregar el nuevo dispositivo
	-Introduciendo un token que deberá guardar
	-Ver el nombre de la versión de la app y guardarlo también

-En el fichero kaaiot.py cambiar las dos variables comentadas arriba (token y versión) por las suyas

-Editar la configuración de la aplicación para el servicio Endpoint Time Series (EPTS) 
	-En el menu de la izquierda opción Aplications->en nuestro dispositivo 
	-Habilitar la opción autoextract de EPTS


