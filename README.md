# BLE-python
Conexión de dispositivos BLE, bombilla Philips Hue (luz blanca y brillo ajustable) y sensor xiaomi Mijia (sensor de temperatura y humedad).
Para el funcionamiento de este proyecto se necesitan los siguietnes requisitos:

-Pyhton instalado superior a 3.7
-Sistema operativo linux
-Raspberry pi 4 (o Raspberry inferior con adaptador bluetooth dotado con BLE)

# Para el sensor de temperatura y humedad
-Instalación de bluez
	 
	 sudo apt install python3 bluez python3-pip
	 pip3 install pybluez
	 pip3 install bluepy

# Para el entorno gráfico de la aplicación:
-Necesario tener instalado pyqt5 y Qt Designer
	sudo apt-get install python-pyqt5
	sudo apt-get install qtcreator pyqt5-dev-tools
	sudo apt-get install python3-pyqt5
	sudo apt-get install pttools5-dev-tools
	pip install pyinstaller 
	sudo apt-get install pyton3-qtawesome (librería para iconos)

# Para la bombilla
	pip3 install pydbus
	Versión de Bluetooth igual o superior a 5.50 (se comprueba con el comando bluetoothctl -v)

# Para la subida de datos a la nube: 
-Necesario tener una cuenta en la página web de cayenne para la subida de resultados, en el siguiente enlace: https://accounts.mydevices.com/auth/realms/cayenne/protocol/openid-connect/auth?response_type=code&scope=email+profile&client_id=cayenne-web-app&state=Ni9R7ZJ0NLdEJUuYqcbTxfOu1ndxWF6QxvMmEXcp&redirect_uri=https%3A%2F%2Fcayenne.mydevices.com%2Fauth%2Fcallback
-Seguir los pasos que se indican una vez te creas la cuenta para instalar cayenne en la raspberry
-Cambiar los datos de usurio, contraseña, cliente, servidor y puerto del fichero cayenne.py por los datos que te muestra después de crearte la cuenta 
-Crear un nuevo proyecto con el nombre cayenne, añadir temperatura, humedad y batería para actualizar los datos
