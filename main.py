
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

from config_test import Config
File = Config("/home/pi/Desktop/Capteur/files")

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
id_cicliste = "ID1_C1"

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
perrorconvert =  b'p8.pic=36' #image for indicate error of convert in the format page (red cross)

pexport =b'va3.val=0' #Start gif for export files in the format page (working gif)
pendexport =b'va3.val=1' #End gif for export files in the format page 
perrorexport =  b'p9.pic=36' #image for indicate error of export in the format page (red cross)

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
        distance = ((recv[2] + recv[3] * 256)*unit)-(distinit*unit)
        return distance

def getGpsData():
    #ser3.write(gp+eof)
    data = ser2.readline().decode('ascii', errors='replace')
    if 'GGA' in data:
            try:
                global_position_sys = pynmea2.parse(data)

                # if global_position_sys.latitude == 0:
                #     ser3.write(gp2+eof)
                # else:
                #     ser3.write(gp+eof)

                return [global_position_sys.latitude,global_position_sys.longitude]
                #move on to the next message if there are problems with the first
            except pynmea2.nmea.ChecksumError as e:
                print('Parse error: {}'.format(e))
            except pynmea2.nmea.ParseError as e:
                print('Unable to parse data{}'.format(e))

def getCamera (timestamp,file_video,r1,r2):
    with picamera.PiCamera () as camera:        
        camera.resolution = (r1,r2)
        camera.framerate = 24
        #camera.start_preview(fullscreen=False,window=(100,200,300,300))
        camera.rotation = 180
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.annotate_text_size=12
        camera.start_recording(file_video)
        #camera.video_stabilization
        start=dt.datetime.now()
        while (dt.datetime.now()-start).seconds < 5000: #time of recording in seconds
            camera.annotate_text=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.wait_recording(0.2)
        camera.stop_recording()
        #ser3.write(P2+eof) #signal of stop recording        

def getMic (timestamp,file_sound):
    time.sleep(0.6)
    outputMic='arecord -D plughw:0 -c1 -r 11025 -f S32_LE -t wav -V mono '+ file_sound
    print (outputMic)
    #subprocess.call(args=[outputMic],shell=True)
    os.system(outputMic)
    #ser3.write(Mic2+eof)

def cleanScreen ():
    ser3.write(P2+eof)
    ser3.write(RP2+eof)
    ser3.write(gp2+eof)
    ser3.write(t2+dist0+eof)
    ser3.write(P42+eof)
    ser3.write(Mic2+eof)

def distanceScreen(distance):
    x = distance
    #print(x)
    y = b'"%d"'%x
    if x == 0:
        ser3.write(P42+eof)
        ser3.write(t2+dist0+eof)
    elif x>0 and x <= 100:
        ser3.write(P4+eof)
        ser3.write(t2+y+eof)
    elif x > 100 and x<= 260:
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
    InPutFolder = Path("/home/pi/Desktop/Capteur/files/video")
    InputSoundFolder = Path("/home/pi/Desktop/Capteur/files/sound")
    OutPutFinalFolder = Path("/home/pi/Desktop/Capteur/files/videostructuredsound")


    original_videos = InPutFolder.files("*.h264")
    original_sound = InputSoundFolder.files("*.wav")
    exported_sound_videos = OutPutFinalFolder.files("*.mp4")

    original_names = [videopath.name.split('.')[0] for videopath in original_videos]
    original_sound_names = [videopath.name.split('.')[0] for videopath in original_sound]
    exported_sound_names = [videopath.name.split('.')[0] for videopath in exported_sound_videos]

    Set1 = set(original_names)
    Set3 = set(original_sound_names)
    Set4 = set(exported_sound_names)

    comp = Set1.intersection(Set4)

    if len(comp)>0 :
        for name in comp :
            out_path = OutPutFinalFolder.joinpath(name+'.mp4')
            os.remove(out_path)

    Videos = InPutFolder.walkfiles("*.h264")
    Commandes = []
    #ffmpeg -i video/ID1_C1_2021_04_21_12_50_40.h264 -i sound/ID1_C1_2021_04_21_12_50_40.wav  -c:v copy -c:a aac -shortest videostructuredsound/ID1_C1_2021_04_21_12_50_40.mp4
    BaseCommande = 'ffmpeg -i "++Inputvideo++" -i "++Inputsound++" -c:v copy -c:a aac -shortest "++Output++"'
    for Video in Videos :
        Inputvideo = Video
        Inputsound = InputSoundFolder.joinpath(Video.name)
        Output = OutPutFinalFolder.joinpath(Video.name)
        thisCommande = BaseCommande.replace("++Inputvideo++",Inputvideo.replace("\\","/")).replace("++Inputsound++",Inputsound.replace(".h264",".wav")).replace("++Output++",Output.replace(".h264",".mp4"))
        print("Executing this command : "+thisCommande)
        os.system(thisCommande)

def ExportFiles ():
    InPutFolder = Path("/home/pi/Desktop/Capteur/files")
    subdirectory = "/media/pi/"

    for root, dirs, files in os.walk(subdirectory):
        for name in files:
            if fnmatch.fnmatch(name, '*.txt'):
                if name == 'LAEQ.txt':
                    Subfolder = root
                    OutPutFolder = Path(Subfolder)
                    print(InPutFolder,OutPutFolder)
                    os.system('cp -r '+ InPutFolder +' '+ OutPutFolder)
                    print (os.path.join(root, name))
                    os.system('umount '+OutPutFolder)
            else:
                print ('Error exportation, no txt file')

def DeleteFiles ():
    Folder1 = Path("/home/pi/Desktop/Capteur/files/distance")
    #Folder2 = Path("/home/pi/Desktop/Capteur/files/videostructured")
    Folder3 = Path("/home/pi/Desktop/Capteur/files/gps")
    Folder4 = Path("/home/pi/Desktop/Capteur/files/video")
    Folder5 = Path("/home/pi/Desktop/Capteur/files/sound")
    Folder6 = Path("/home/pi/Desktop/Capteur/files/videostructuredsound")

    distanceF = Folder1.files("*.csv")
    #videostructuredF = Folder2.files("*.mp4")
    gpsf = Folder3.files("*.csv")
    videoF = Folder4.files("*.h264")
    soundf = Folder5.files("*.wav")
    videoFS = Folder6.files("*.mp4")

    Set1 = set(distanceF)
    #Set2 = set(videostructuredF)
    Set3 = set(gpsf)
    Set4 = set(videoF)
    Set5 = set(soundf)
    Set6 = set(videoFS)

    #print (Set1)

    if len(Set1)>0 :
        for name in Set1 :
            os.remove(name)

    if len(Set3)>0 :
        for name in Set3 :
            os.remove(name)

    if len(Set4)>0 :
        for name in Set4 :
            os.remove(name)

    if len(Set5)>0 :
        for name in Set5 :
            os.remove(name)

    if len(Set6)>0 :
        for name in Set6 :
            os.remove(name)

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

def create_files(id_cicliste, timestamp):
    file_video=File.new_distance(id_cicliste,timestamp)
    print(file_video)
    file_sound=File.new_video(id_cicliste,timestamp)
    print(file_sound)
    file_gps=File.new_gps(id_cicliste,timestamp)
    print(file_gps)
    file_distance=File.new_sound(id_cicliste,timestamp)
    print(file_distance)

#####################
#Generer les commandes
#####################


if __name__ == '__main__':

    timestamp = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 
    create_files(id_cicliste, timestamp)
    a, b, c, d = File.start(id_cicliste,timestamp)
    print (a, b,c,d)



    #Signal of connected device
    ser3.write(page1+eof) # acces a la page 1 / menu

    while True: #page 1 /  menu
        pagecounter=ser3.readline()         
        HourScreenMenu () #Hour
        DateScreenMenu () #Date

        while pagecounter==b'page2': #page 2 /  record
            #Clean the screen
            cleanScreen ()
            ser3.write(RP1+eof) #Rpi connected

            #Reading input of screen touch nextion (waiting: start)
            while start==b'':
                start=ser3.readline() #reading serial port from the screen touch             
                HourRecordMenu () #Hour
                
                if start==b'start':    #start process of: camera, gps and distance sensor.                 

                    timestamp = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 
                    file_video, file_sound, file_distance, file_gps= File.start(id_cicliste,timestamp)   


                    previousGpsTime = 0
                    previousDistTime = 0                
                    ser.open()
                    ser2.open()
                    print("Begin recording video")
                    ser3.write(P1+eof) #signal of recording video                               
                    cam=Process(target = getCamera, args=(timestamp,file_video,r1,r2,))
                    cam.start()

                    print("Begin recording audio")
                    ser3.write(Mic+eof) #signal of recording audio 
                    mic=Process(target = getMic, args=(timestamp,file_sound))
                    mic.start()

                    #Prepare de file csv for writing                    
                    with open('/home/pi/Desktop/Capteur/files/distance/ID1_C1_{}.csv'.format(timestamp), 'a') as distance_csv:
                        distance_csv.write("time,distance\n")
                    with open('/home/pi/Desktop/Capteur/files/gps/ID1_C1_{}.csv'.format(timestamp), 'a') as GPS_csv:
                        GPS_csv.write("time,latitude,longitude\n")

                    while Record==True:
                        stop=ser3.readline()
                        HourRecordMenu ()
                        hour=dt.datetime.now().strftime('%H:%M:%S.%f')
                        currentTime =int(round(time.perf_counter()*1000))

                        distance=getTFminiData(unit,distinit)
                        distanceScreen(distance)
                        if distance>0 and distance <= maximumDistance:
                            #print(hour,distance)                            
                            with open('/home/pi/Desktop/Capteur/files/distance/ID1_C1_{}.csv'.format(timestamp), 'a') as distance_test:
                                distance_test.write(hour + ',' + str(distance) +  '\n')
                            #file1.write(hour + ',' + str(distance) +  '\n')

                        gps = None                        

                        if currentTime - previousGpsTime > gpsperiod:
                            gps = getGpsData()
                            ser3.write(gp+eof)
                            print(gps)
                            previousGpsTime = currentTime

                        if gps!= None:
                            print(hour,gps)
                            gpsScreen(gps)
                            with open('/home/pi/Desktop/Capteur/files/gps/ID1_C1_{}.csv'.format(timestamp), 'a') as GPS_csv:
                                GPS_csv.write(str(hour) + ',' + str(gps[0]) + ',' + str(gps[1]) +  '\n')

                        if stop==b'stop':
                            Record=False
                            print("End recording video")
                            cam.terminate()
                            cam.join()
                            subprocess.call(['pkill arecord'],shell=True)
                            #os.system()
                            print("End recording audio")
                            mic.terminate()
                            mic.join()
                            start=0
                            ser.close()
                            ser2.close()
                            pagecounter=b'page2'

                        if stop==b'page1':
                            Record=False
                            print("End recording video - page1")
                            cam.terminate()
                            cam.join()
                            subprocess.call(['pkill arecord'],shell=True)
                            #os.system('pkill arecord')
                            print("End recording audio - page1")
                            mic.terminate()
                            mic.join()
                            start=0
                            ser.close()
                            ser2.close()
                            pagecounter=b''

            #return to 0
            cleanScreen()
            Record=True
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

            if capture==b'page1': #in/out menu setup
                pagecounter=b''

            if capture==b'capture': #Reading distance of reference
                try:
                    ser.open()
                    distanceref =getTFminiDataRef(unit)
                    y = b'"%d"'%distanceref
                    if distanceref > 0 and distanceref <= 30:
                        ser3.write(t8+y+eof)
                        distinit=distanceref*unit
                        print ('Initial distance:',distinit)
                        ser.close()
                    ser.close()
                except:
                    pass
                finally:
                    pass

            if capture==b'convert': #convert button
                print ("Begin convert files")
                ser3.write(pconvert+eof)
                try:
                    ExportVideo ()
                    ser3.write(pendconvert+eof)
                    ser3.write(Finishconvert+eof)
                except:
                    ser3.write(perrorconvert+eof)
                finally:
                    pass                
                print ("End convert files")
                    
            if capture==b'export': #export button
                print ("Begin export files")
                ser3.write(pexport+eof)
                try:
                    ExportFiles ()
                    ser3.write(pendexport+eof)
                    ser3.write(Finishexport+eof)
                except:
                    ser3.write(perrorexport+eof)
                finally:
                    pass
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
                try: 
                    DeleteFiles ()
                    ser3.write(pfinish+eof)
                    print ("End delete files")
                except:
                    pass
                finally:
                    pass 
                pagecounter=b''
                delete=b''                
                ser3.write(page1+eof)
                    




