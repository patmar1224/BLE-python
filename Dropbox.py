import dropbox

def subir_dropbox():
    #Subir un archivo a dropbox pero primero se borra para poder actualizarlo cada vez que se suba
    file_from = '/home/pi/BLE-python/Cargar_Datos_Antiguos.txt'
    file_to = '/Aplicaciones/BLE-python/Recogida_Datos_Sensor.txt'
    dbx = dropbox.Dropbox('w0drjFywERoAAAAAAAAAAZvVqIblxMdWb1m3pkqjv4AWQUyjgblMejpynhy7zsnN')
    #dbx.files_delete(file_to)
    dbx.files_upload(open(file_from, 'rb').read(), file_to)
    
#subir_dropbox()