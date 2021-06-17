from time import sleep
from pydbus import SystemBus

BLUEZ_SERVICE = 'org.bluez'
BLUEZ_DEV_IFACE = 'org.bluez.Device1'
BLUEZ_CHR_IFACE = 'org.bluez.GattCharacteristic1'


class Central:

    def __init__(self, address):
        self.bus = SystemBus()
        self.mngr = self.bus.get(BLUEZ_SERVICE, '/')
        self.dev_path = self._from_device_address(address)
        self.device = self.bus.get(BLUEZ_SERVICE, self.dev_path)
        self.chars = {}

    def _from_device_address(self, addr):
        """Look up D-Bus object path from device address"""
        mng_objs = self.mngr.GetManagedObjects()
        for path in mng_objs:
            dev_addr = mng_objs[path].get(BLUEZ_DEV_IFACE, {}).get('Address', '')
            if addr.casefold() == dev_addr.casefold():
                return path

    def _get_device_chars(self):
        mng_objs = self.mngr.GetManagedObjects()
        for path in mng_objs:
            chr_uuid = mng_objs[path].get(BLUEZ_CHR_IFACE, {}).get('UUID')
            if path.startswith(self.dev_path) and chr_uuid:
                self.chars[chr_uuid] = self.bus.get(BLUEZ_SERVICE, path)


    def connect(self):
        """
        Connect to device.
        Wait for GATT services to be resolved before returning
        """
        self.device.Connect()
        while not self.device.ServicesResolved:
            sleep(0.5)
        self._get_device_chars()

    def disconnect(self):
        """Disconnect from device"""
        self.device.Disconnect()

    def char_write(self, uuid, value):
        """Write value to given GATT characteristic UUID"""
        if uuid.casefold() in self.chars:
            self.chars[uuid.casefold()].WriteValue(value, {})
        else:
            raise KeyError(f'UUID {uuid} not found')

    def char_read(self, uuid):
        """Read value of given GATT characteristic UUID"""
        if uuid.casefold() in self.chars:
            return self.chars[uuid.casefold()].ReadValue({})
        else:
            raise KeyError(f'UUID {uuid} not found')

def configuracion_bombilla(mac):
    global device_address
    global light_state
    global light_brillo
    device_address = mac
    light_state = '932c32bd-0002-47a2-835a-a8d455b859dd'
    light_brillo = '932c32bd-0003-47a2-835a-a8d455b859dd'

def apagar ():
    dev = Central(device_address )
    dev.connect()
    dev.char_write(light_state , [0])
    print(dev.char_read(light_state ))
    dev.disconnect()

def encender ():
    dev = Central(device_address )
    dev.connect()
    dev.char_write(light_state , [1])
    print(dev.char_read(light_state ))
    dev.disconnect()

#El brillo va de 1 a 254
def brillo (bri):
    dev = Central(device_address )
    dev.connect()
    dev.char_write(light_brillo , [bri])
    dev.disconnect()
    
# MAC='CD:D2:E9:40:11:BC'
# configuracion_bombilla(str(MAC))
# apagar()