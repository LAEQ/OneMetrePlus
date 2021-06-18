# -*- coding: utf-8 -*


"""
Created on Friday July 07 10:13:28 2020

@author: AndresH
"""


#Code pour verifier fonctionnement et connexion du tfmini plus lidar / capteur de distance

import serial
import time
import datetime as dt


#Il faut verifier le nombre du port USB avant de proceder

ser = serial.Serial("/dev/ttyUSB0", 115200)
timestamp = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')


def getTFminiData():
    while True:
        recv = ser.read(9)
        ser.reset_input_buffer() 
        #time.sleep (0.5)
        if recv[0] == 0x59 and recv[1] == 0x59:     #python3
            distance = (recv[2] + recv[3] * 256)-3
            strength = recv[4] + recv[5] * 256
            t = time.localtime()
            timesystem = time.strftime("%H:%M:%S",t)
            print( timesystem, ',', distance, ',', strength)
            ser.reset_input_buffer()

#####################
#Generer les commandes
#####################

if __name__ == '__main__':
    
    getTFminiData()
        
