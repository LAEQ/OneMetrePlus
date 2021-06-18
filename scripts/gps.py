#!/usr/bin/python3

"""
Created on Friday July 07 10:13:28 2020

@author: AndresH
"""

#Code pour verifier fonctionnement et connexion du GPS

import pynmea2
import os
import time
import sys
import glob
import serial
import time
import datetime as dt


#Il faut verifier le nombre du port USB avant de proceder

ser2 = serial.Serial('/dev/ttyUSB1', 9600) #gps
#timestamp = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')



def get_gps_data(timestamp):
    file = open('/home/pi/captures/gps/ID1_AH_{}.csv'.format(timestamp),'a+')
    file.write("time,latitude,longitude\n")
    while True:
        data = ser2.readline().decode('ascii', errors='replace')
        if 'GGA' in data:
            global_position_sys = pynmea2.parse(data)
            hour=dt.datetime.now().strftime('%H:%M:%S')
            file.write(str(hour) + ',' + str(global_position_sys.latitude) + ',' + str(global_position_sys.longitude) +'\n')
            print (hour,global_position_sys.latitude,global_position_sys.longitude)
            
#####################
#Generer les commandes
#####################
            
if __name__ == '__main__':
    timestamp = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    get_gps_data(timestamp)


