import serial
import time

arduinoData = serial.Serial('COM4',
                            9600)  # aqui pone el puerto (o algo asi se llama xd) donde esta conectado el arduino, normalmente es una salida usb


def led_on():
    arduinoData.write('1'.encode())


def led_off():
    arduinoData.write('0'.encode())


def open_file():
    arduinoData.write(open("/Users/migue/Desktop/drawing.gcode",
                           "rb").read())  # esto es la direccion donde el mae va buscar el gcode, en nuestro caso se va generar en la carpeta Image, pero ahi yo lo tenia en una direccion del escritorio porque soy un vulgar xd, cualquier vara dentro de Image ya hay un gcode para que lo intente ejecutar


t = 0
time.sleep(2)

open_file()
print("done")
