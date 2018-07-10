# -*- coding: cp1252 -*-

#         _\|/_     A ver...  ¿que tenemos por aqui?
#         (O-O) 
# -----oOO-(_)-OOo----------------------------------------------------


#######################################################################
# ******************************************************************* #
# *                                                                 * #
# *                   Autor:  Eulogio López Cayuela                 * #
# *                                                                 * #
# *           Utilidad para el uso de puertos Serie en python       * #
# *                                                                 * #
# *                  Versión 1.0   Fecha: 27/04/2016                * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################




#--------------------------------------------------------
# IMPORTACION DE MODULOS
#--------------------------------------------------------

import sys         #Conocer el tipo de sistema operativo
import time        #manejo de funciones de tiempo (fechas, horas, pausas...)
import serial      #libreria Serial para comunicar con Arduino




#====================================================================================================
# INICIO DEL BLOQUE DE DEFINICION DE FUNCIONES
#====================================================================================================

def detectar_PuertoSerie():
    '''
    Funcion para facilitar la deteccion del puerto Serie en distintos sistemas operativos
    Escanea los posibles puertos y retorna el nombre del puerto con el que consigue comunicarse
    '''

    #Reconocer el tipo de sistema operativo
    sistemaOperativo = sys.platform
    
    #Definir los prefijos de los posibles puertos serie disponibles tanto en linux como windows
    puertosWindows = ['COM']
    puertosLinux = ['/dev/ttyUSB', '/dev/ttyACM', '/dev/ttyS', '/dev/ttyAMA','/dev/ttyACA']
    
    puertoSerie = None
    if (sistemaOperativo == 'linux2'):
        listaPuertosSerie = puertosLinux
    else:
        listaPuertosSerie = puertosWindows

    for puertoTestado in listaPuertosSerie:
        for n in range(20):
            try:
                # intentar crear una instancia de Serial para 'dialogar' con ella
                nombrePuertoSerie = puertoSerie+'%d' %n
                serialTest = serial.Serial(nombrePuertoSerie, 9600)

                '''  este bloque es opcional por si queremos por ejempo, que ante varios dispositivos conectados
                obtener el nombre del puerto en el que hay uno en concreto que estemos buscando.
                Cosa que podemos hacer dialogando con el y esperando una respuesta conocida
                '''
##                datos_recibidos = None
##                datos_recibidos = consultar_PuertoSerie(serialTest, b'dato de muestra')# El prefijo b (byte) es opcional en python 2.x pero obligatorio en 3.x
##                serialTest.close()
##                if datos_recibidos == "patron deseado":
##                    return puertoSerie

                #devolver el primer puerto disponible. Si queremos devolver uno en concreto, comentar estas dos lineas y descomentar el bloque anterior
                serialTest.close()
                return puertoSerie

            except Exception as e:
                pass
                #descometnar si se desea conocer el eror (obviamente es que el puerto no esta disponible)
                #print e
        
    return None #si llegamos a este punto es que no hay puerto serie disponible


# --------------------------------------------

def consultar_PuertoSerie(SerialPort, peticion): # con esta notacion: b'*') --> El prefijo b (byte) es opcional en python 2.x pero obligatorio en 3.x
    '''
    Funcion para acceso a PuertoSerie y obtencion de datos
    version mejorada para evitar errores de comunicacion
    ante eventuales fallos de la conexion.
    '''

    try:
        SerialPort.flushInput()         # flush input buffer, eliminar posibles restos de lecturas anteriores
        SerialPort.flushOutput()        # flush output buffer, abortar comunicaciones salientes que puedan estar a medias

    except Exception as e:
        print (epochDate(time.time()), e)
        print("error borrando datos del puerto Serie")
 

    # ** INICIO bloque de consulta  ** 
    try:
        SerialPort.write(peticion)      # El prefijo b (byte) es opcional en python 2.x pero obligatorio en 3.x
        time.sleep(0.25)                # pausa opcional, para que el dispositivo reaccione y deje la respuesta en el puerto Serie
        if (SerialPort.inWaiting()>0):  # revisar si hay datos en el puerto serie
            datos_leidos_en_SerialPort = SerialPort.readline() #leer una cadena desde el el puerto serie
            try:
                pass
                #este try es por si se desea procesar/comprobar los datos leidos antes de devolverlos

            except Exception as e:
                print("Datos no validos")
                return None

    except Exception as e:
        print("\n == CONEXION PERDIDA == ")


    return datos_leidos_en_SerialPort

#----------------------------------------------------------------------------------------------------
#  FIN DEL BLOQUE DE DEFINICIÒN DE FUNCIONES
#----------------------------------------------------------------------------------------------------





#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

#   INICIO DEL PROGRAMA COMO TAL

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm




#crear un pueto serie para la comunicacion, si encontramos puerto didponible
puertoDetectado = detectar_PuertoSerie() #detactamos automaticamente el puerto

if (puertoDetectado != None):
    mi_puerto_Serie = serial.Serial(puertoDetectado, 9600) #usamos el puerto detectado
    print (" ** DISPOSITIVO CONECTADO EN " + puertoDetectado + " ** ")
else:
    print (" == DISPOSITIVO NO PRESENTE == ")


#bucle para leer continuamente el puerto
while puertoDetectado:
    datos_recibidos = consultar_PuertoSerie(mi_puerto_Serie, b'peticion')# El prefijo b (byte) es opcional en python 2.x pero obligatorio en 3.x
    print(datos_recibidos)




