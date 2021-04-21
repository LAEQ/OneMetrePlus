
"""
Created on Friday July 07 10:53:28 2020

@author: AndresH
"""

#Code pour capteur de distance LAEQ (laboratoire d'equite environnemental - Montréal / Québec)

#####################
#Library
#####################

from threading import Thread
from multiprocessing import Process
import pynmea2
import os
import sys
import glob
import serial
import time
import datetime as dt
import picamera
import subprocess
from path import Path
import fnmatch

#####################
#Global variables
#####################
tfminiperiod = 1
gpsperiod = 250
touchperiod = 200
maximumDistance = 300
start=b''
Record=True
x=0
distanceref=0
unit=1 #cm ref
cm = 1
inch=0.393701
distinit=0 #initial distance
# Camera resolution 
r1 = 400 #camera resolution
r2 = 300 #camera resolution

#####################
#Serial Instructions for screen
#####################
eof = b'\xff\xff\xff'
t2 = b't2.txt=' #text object for distance in the record page
t8 = b't8.txt='
t14 = b't14.txt=' #text object for hour in the record page
t15 = b't15.txt=' #text object for hour in the main menu
t16 = b't0.txt=' #text object for date in the main menu

P1 = b'p1.pic=0' #image for recording in the record page (red circle)
P2=b'p1.pic=2' #image standard for indicator of record (black square)

gp= b'p2.pic=1' #image for GPS in the record page (target)
gp2=b'p2.pic=2' #image standard for indicator (black square)

RP1=b'p3.pic=6' #image for raspberry connection in the record page (raspberry pi icon)
RP2=b'p3.pic=2' #image standard for indicator (black square)

P4 = b'p4.pic=7' #image for distance < 100 cm  in the record page (Warning sign)
P42= b'p4.pic=8' #image standard for indicator (black square)

Mic=b'p12.pic=32' #image for microphone in the record page (mic icon)
Mic2=b'p12.pic=2' #image standard for indicator (black square)

pdelete=b'va1.val=0'  #Start gif for delete files in the delete page (working gif)
pfinish=b'va1.val=1' #End gif for delete files in the delete page 

pconvert =b'va1.val=0'  #Start gif for convert files in the format page (working gif)
pendconvert =b'va1.val=1' #End gif for convert files in the format page 

pexport =b'va3.val=0' #Start gif for export files in the format page (working gif)
pendexport =b'va3.val=1' #End gif for export files in the format page 

Finishconvert= b'p8.pic=26' #image for indicate that convert is finish in the format page (green circle)
Finishexport= b'p9.pic=26' #image for indicate that export is finish in the format page (green circle)
Usbplug= b'p9.pic=31' #image for indicate that usb is connected and have the file LAEQ.txt in the format page (green ok)

dist0=b'"000"' #text object for reinitialize the distance in the record page

page0= b'page 0' #page number for the animation LAEQ 
page1= b'page 1' #page number for the main menu
page2= b'page 2' #page number for the record page

picerror= b'p18.pic=35' #error image during recording in the record page (red rectangle with word error)

pagecounter=b'' #page counter between raspberry pi and nextion screen 

subdirectory = "/media/pi/"

#####################
#Ports USB
#####################
ser = serial.Serial("/dev/ttyUSB0", 115200) #tfmini
ser.close()
ser2 = serial.Serial('/dev/ttyUSB1', 9600) #gps
ser2.close()
ser3 = serial.Serial(port='/dev/ttyUSB2',baudrate=115200, #ecran
        parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,timeout=0.01)


#####################
#Fonctions
#####################
def getTFminiDataRef(unit):
    recv = ser.read(9)
    ser.reset_input_buffer()
    if recv[0] == 0x59 and recv[1] == 0x59:
        distance = ((recv[2] + recv[3] * 256)*unit)
        return distance

def getTFminiData(unit,distinit):
    recv = ser.read(9)
    ser.reset_input_buffer()
    if recv[0] == 0x59 and recv[1] == 0x59:
        distance = ((recv[2] + recv[3] * 256)*unit)-(3*unit)-(distinit*unit)
        return [distance]

def getGpsData():
    ser3.write(gp+eof)
    data = ser2.readline().decode('ascii', errors='replace')
    if 'GGA' in data:
            try:
                global_position_sys = pynmea2.parse(data)

                if global_position_sys.latitude == 0:
                    ser3.write(gp2+eof)
                else:
                    ser3.write(gp+eof)

                return [global_position_sys.latitude,global_position_sys.longitude]
                #move on to the next message if there are problems with the first
            except pynmea2.nmea.ChecksumError as e:
                print('Parse error: {}'.format(e))
            except pynmea2.nmea.ParseError as e:
                print('Unable to parse data{}'.format(e))

def getCamera (timestamp,r1,r2):
    with picamera.PiCamera () as camera:
        print("Start video")
        camera.resolution = (r1,r2)
        camera.framerate = 24
        #camera.start_preview(fullscreen=False,window=(100,200,300,300))
        camera.rotation = 180
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.annotate_text_size=12
        ser3.write(P1+eof) #signal of recording
        camera.start_recording('/home/pi/Desktop/Capteur/files/video/ID1_C1_{}.h264'.format(timestamp))
        #camera.video_stabilization
        start=dt.datetime.now()
        while (dt.datetime.now()-start).seconds < 5000: #time of recording in seconds
            camera.annotate_text=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.wait_recording(0.2)
        camera.stop_recording()
        ser3.write(P2+eof) #signal of stop recording
        print("End video")

def getMic (timestamp):
    time.sleep(0.6)
    ser3.write(Mic+eof) #signal of recording
    outputMic='arecord -D plughw:0 -c1 -r 11025 -f S32_LE -t wav -V mono '+'/home/pi/Desktop/Capteur/files/sound/ID1_C1_'+timestamp+'.wav'
    print (outputMic)
    #subprocess.call(args=[outputMic],shell=True)
    os.system(outputMic)
    ser3.write(Mic2+eof)

def cleanScreen ():
    ser3.write(P2+eof)
    ser3.write(RP2+eof)
    ser3.write(gp2+eof)
    ser3.write(t2+dist0+eof)
    ser3.write(P42+eof)
    ser3.write(Mic2+eof)

def distanceScreen(distance):
    x = distance[0]
    #print(x)
    y = b'"%d"'%x
    if x == 0:
        ser3.write(P42+eof)
        ser3.write(t2+dist0+eof)
    elif x>0 and x <= 30:
        ser3.write(P4+eof)
        ser3.write(t2+y+eof)
    elif x > 30 and x<= 260:
        ser3.write(P42+eof)
        ser3.write(t2+y+eof)
    elif x == None:
        Ser3.write(P42+eof)
        ser3.write(t2+dist0+eof)
    else:
        ser3.write(P42+eof)
        ser3.write(t2+dist0+eof)


    #print (y)

def gpsScreen(gps):
    x=gps[0]
    if x == 0:
        ser3.write(gp2+eof)
    else:
        ser3.write(gp+eof)

def ExportVideo ():
    subprocess.run(['python3', '/home/pi/exportvideo.py'])

def ExportFiles ():
    subprocess.run(['python3', '/home/pi/exportdata.py'])

def DeleteFiles ():
    subprocess.run(['python3', '/home/pi/delete.py'])

def HourScreenMenu ():
    hour=dt.datetime.now().strftime('%H:%M:%S')
    hourstr = '"%s"'%hour
    hourstrb = bytes(hourstr, 'utf-8')
    ser3.write(t15+hourstrb+eof)

def DateScreenMenu ():
    date=dt.datetime.now().strftime('%Y-%m-%d')
    datestr = '"%s"'%date
    datestrb = bytes(datestr, 'utf-8')
    ser3.write(t16+datestrb+eof)

def HourRecordMenu ():
    hour=dt.datetime.now().strftime('%H:%M:%S')
    hourstr = '"%s"'%hour
    hourstrb = bytes(hourstr, 'utf-8')
    ser3.write(t14+hourstrb+eof)

def PresenceUsb ():
    #Icon ok for usb connected
    for root, dirs, files in os.walk(subdirectory):
        for name in files:
            if fnmatch.fnmatch(name, '*.txt'):
                if name == 'LAEQ.txt':
                    ser3.write(Usbplug+eof)

#####################
#Generer les commandes
#####################


if __name__ == '__main__':

    #Signal of connected device
    ser3.write(page1+eof) # acces a la page 1 / menu

    while True: #page 1 /  menu
        pagecounter=ser3.readline()
        #Hour and date
        HourScreenMenu ()
        DateScreenMenu ()

        while pagecounter==b'page2': #page 2 /  record
            #Clean the screen
            cleanScreen ()
            ser3.write(RP1+eof)

            #Reading input of screen touch nextion (waiting: start)
            while start==b'' or start==b'stop':
                start=ser3.readline()
                #print ("Waiting", start)
                HourRecordMenu ()

                #start process of: camera, gps and distance sensor.
                if start==b'start':
                    print("Begin recording")
                    previousGpsTime = 0
                    previousDistTime = 0
                    timestamp = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                    ser.open()
                    ser2.open()
                    cam=Process(target = getCamera, args=(timestamp,r1,r2,))
                    cam.start()
                    mic=Process(target = getMic, args=(timestamp,))
                    mic.start()

                    #Prepare de file csv for writing
                    file1 = open('/home/pi/Desktop/Capteur/files/distance/ID1_C1_{}.csv'.format(timestamp),'a+')
                    file1.write("time,distance\n")
                    file2 = open('/home/pi/Desktop/Capteur/files/gps/ID1_C1_{}.csv'.format(timestamp),'a+')
                    file2.write("time,latitude,longitude\n")

                    while Record==True:

                        stop=ser3.readline()
                        HourRecordMenu ()
                        hour=dt.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                        currentTime =int(round(time.perf_counter()*1000))

                        distance=getTFminiData(unit,distinit)
                        distanceScreen(distance)
                        if distance[0]>0 and distance[0] <= maximumDistance:
                            print(hour,distance[0])
                            file1.write(str(hour) + ',' + str(distance[0]) +  '\n')

                        gps = None

                        if currentTime - previousGpsTime > gpsperiod:
                            gps = getGpsData()
                            print(gps)
                            previousGpsTime = currentTime

                        if gps!= None:
                            print(hour,gps)
                            #gpsScreen(gps)
                            file2.write(str(hour) + ',' + str(gps[0]) + ',' + str(gps[1]) +  '\n')

                        if stop==b'stop':
                            Record=False
                            cam.terminate()
                            cam.join()
                            subprocess.call(['pkill arecord'],shell=True)
                            #os.system()
                            mic.terminate()
                            mic.join()
                            start=0
                            file1.close()
                            file2.close()
                            ser.close()
                            ser2.close()
                            pagecounter=b'page2'
                            print ('Stop recording')


                        if stop==b'page1':
                            Record=False
                            cam.terminate()
                            cam.join()
                            subprocess.call(['pkill arecord'],shell=True)
                            #os.system('pkill arecord')
                            mic.terminate()
                            mic.join()
                            start=0
                            file1.close()
                            file2.close()
                            ser.close()
                            ser2.close()
                            pagecounter=b''
                            print ('Stop recording')

                        #time.sleep(0.01)
                        #print(start)

                if start==b'page1': #In case of in/out of page2
                    start=2
                    #pagecounter=b''

            #return to 0
            cleanScreen()
            Record=True
            if start==2:
                pagecounter=b''
            start=b''

        while pagecounter==b'page3': #page 3 /  setup
            #Reading input of screen touch nextion (waiting: Value)
            Format=ser3.readline()
            #print ("config", Format)
            if Format==b'in':
                unit = inch
                print (unit)
            if Format==b'cm':
                unit = cm
                print (unit)
            if Format==b'page1':
                pagecounter=b''

        while pagecounter==b'page4': #page 4 /  format
            #Reading input of screen touch nextion (waiting for distance ref, camera resolution, convert or export)
            capture=ser3.readline()
            #identifies the presence of a connected usb
            PresenceUsb ()

            if capture==b'capture': #Reading distance of reference
                ser.open()
                distanceref =getTFminiDataRef(unit)
                y = b'"%d"'%distanceref
                if distanceref > 0 and distanceref <= 30:
                    ser3.write(t8+y+eof)
                    distinit=distanceref*unit
                    print ('Initial distance:',distinit)
                    ser.close()
                ser.close()

            if capture==b'page1': #in/out menu setup
                pagecounter=b''

            if capture==b'convert': #convert button
                print ("Begin convert files")
                ser3.write(pconvert+eof)
                ExportVideo ()
                ser3.write(pendconvert+eof)
                ser3.write(Finishconvert+eof)
                print ("End convert files")
                    
            if capture==b'export': #export button
                print ("Begin export files")
                ser3.write(pexport+eof)
                ExportFiles ()
                ser3.write(pendexport+eof)
                ser3.write(Finishexport+eof)
                print ("End export files")

            if capture==b'800': #Resolution button 800x600
                r1 = 800
                r2 = 600
                print ("Camera resolution:",r1,r2)

            if capture==b'600': #Resolution button 600x450
                r1 = 600
                r2 = 450
                print ("Camera resolution:",r1,r2)

            if capture==b'400': #Resolution button 400x300 for default
                r1 = 400
                r2 = 300
                print ("Camera resolution:",r1,r2)

        while pagecounter==b'page5': #page 5 /  Delete files
            #Reading input of screen touch nextion (waiting for delete files command)
            delete=ser3.readline()

            if delete==b'page1': #in/out menu setup
                pagecounter=b''

            if delete==b'delete': #Delete button
                print ("Begind delete files")
                ser3.write(pdelete+eof)
                DeleteFiles ()
                ser3.write(pfinish+eof)
                pagecounter=b''
                delete=b''
                print ("End delete files")
                ser3.write(page1+eof)
                    




