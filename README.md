# BLE-python
Conexión de dispositivos BLE, bombilla Philips Hue (luz blanca y brillo ajustable) y sensor xiaomi Mijia (sensor de temperatura y humedad).
Para el funcionamiento de este proyecto se necesitan los siguietnes requisitos:
·Pyhton instalado superior a 3.7
·Para el sensor de temperatura y humedad
	-Instalación de bluez
	 sudo apt install python3 bluez python3-pip
	 pip3 install pybluez
	 pip3 install bluepy

·Para el entorno gráfico de la aplicación:
	-sudo apt-get install python-pyqt5
	-sudo apt-get install qtcreator pyqt5-dev-tools
	-sudo apt-get install python3-pyqt5
	-sudo apt-get install pttools5-dev-tools
	-pip install pyinstaller 
	-sudo apt-get install pyton3-qtawesome (librería para iconos)
·Para la bombilla
	-pip3 install pydbus
	-Versión de Bluetooth igual o superior a 5.50 (se comprueba con el comando bluetoothctl -v)
