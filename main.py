
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
from utils.config import Config
from utils.filemanager import FileManager
from utils.screen import Screen
from utils.tools import get_date, get_time

gps_period_capture = 300
maximum_sensor_distance = 300  #unit in cm
# Camera resolution 
camera_resolution_width = 480 #camera resolution
camera_resolution_height = 270 #camera resolution
start=b''
record=True
initial_distance=0 #initial distance
unit=1 #cm ref
cm = 1
inch=0.393701
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

page_counter=b'' #page counter between raspberry pi and nextion screen

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
def get_tfmini_data_ref(unit):
    recv = ser.read(9)
    ser.reset_input_buffer()
    if recv[0] == 0x59 and recv[1] == 0x59:
        distance = ((recv[2] + recv[3] * 256)*unit)
        return distance

def get_tfmini_data(unit,initial_distance):
    recv = ser.read(9)
    ser.reset_input_buffer()
    if recv[0] == 0x59 and recv[1] == 0x59:
        distance = ((recv[2] + recv[3] * 256)*unit)-(initial_distance*unit)
        return distance

def get_gps_data():
    data = ser2.readline().decode('ascii', errors='replace')
    if 'GGA' in data:
            try:
                global_position_sys = pynmea2.parse(data)
                return [global_position_sys.latitude,global_position_sys.longitude]
            except pynmea2.nmea.ChecksumError as e:
                print('Parse error: {}'.format(e))
            except pynmea2.nmea.ParseError as e:
                print('Unable to parse data{}'.format(e))
            finally:
                pass

def get_gps_data2(file_gps):
    while True:
        data = ser2.readline().decode('ascii', errors='replace')
        if 'GGA' in data:
                try:
                    global_position_sys = pynmea2.parse(data)
                    hour=dt.datetime.now().strftime('%H:%M:%S.%f')
                    lat = global_position_sys.latitude
                    gps_screen(lat)
                    print (hour,global_position_sys.latitude,global_position_sys.longitude)
                    with open(file_gps, 'a') as gps_csv:
                        gps_csv.write(str(hour) + ',' + str(global_position_sys.latitude) + ',' + str(global_position_sys.longitude) +  '\n')
                except pynmea2.nmea.ChecksumError as e:
                    print('Parse error: {}'.format(e))
                except pynmea2.nmea.ParseError as e:
                    print('Unable to parse data{}'.format(e))
                finally:
                    pass
        else:
            ser3.write(gp+eof)

def get_camera(file_video,camera_resolution_width,camera_resolution_height):
    with picamera.PiCamera () as camera:
        camera.resolution = (camera_resolution_width,camera_resolution_height)
        camera.framerate = 25
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

def get_microphone(timestamp,file_sound):
    time.sleep(0.6)
    outputMic='arecord -D plughw:1 -c1 -r 11025 -f S32_LE -t wav -V mono '+ file_sound
    print (outputMic)
    os.system(outputMic)

def distance_screen(distance):
    y = b'"%d"'%distance
    if distance == 0:
        ser3.write(P42+eof)
        ser3.write(t2+dist0+eof)
    elif distance>0 and distance <= 100:
        ser3.write(P4+eof)
        ser3.write(t2+y+eof)
    elif distance > 100 and distance<= 260:
        ser3.write(P42+eof)
        ser3.write(t2+y+eof)
    elif distance == None:
        ser3.write(P42+eof)
        ser3.write(t2+dist0+eof)
    else:
        ser3.write(P42+eof)
        ser3.write(t2+dist0+eof)

def gps_screen(lat):
    if lat == 0:
        ser3.write(gp2+eof)
    else:
        ser3.write(gp+eof)

def convert_video(config):
    list_export=config.get_export()
    if len(list_export)>0 :
        for element in list_export:
            os.remove(element)

    list_videos=config.get_videos()
    BaseCommande = 'ffmpeg -i "++input_video++" -i "++input_sound++" -c:v copy -c:a aac -shortest "++out_put++"'
    for video in list_videos :
        input_video = video
        input_sound = input_video.replace('video','sound')
        out_put = input_video.replace('video','export')
        thisCommande = BaseCommande.replace("++input_video++",input_video).replace("++input_sound++",input_sound.replace(".h264",".wav")).replace("++out_put++",out_put.replace(".h264",".mp4"))
        print("Executing this command : "+thisCommande)
        os.system(thisCommande)

def export_files():
    input_folder = Path("/home/pi/Sensor")
    sub_directory = "/media/pi/"

    for root, dirs, files in os.walk(sub_directory):
        for name in files:
            if fnmatch.fnmatch(name, '*.txt'):
                if name == 'LAEQ.txt':
                    sub_folder = root
                    output_folder = Path(sub_folder)
                    print(input_folder,output_folder)
                    os.system('cp -r '+ input_folder +' '+ output_folder)
                    print (os.path.join(root, name))
                    os.system('umount '+output_folder)
                    return (True)
            else:
                print ('Error export, no txt file in usb')
    else:
        return (False)

def delete_files(config):
    pass
#     list_file= config.get_all_files()
#     for element in list_file:
#         os.remove(element)


def menu_record_hour():
    hour=dt.datetime.now().strftime('%H:%M:%S')
    hourstr = '"%s"'%hour
    hourstrb = bytes(hourstr, 'utf-8')
    ser3.write(t14+hourstrb+eof)

def usb_connected():
    subdirectory = "/media/pi/"
    #Icon ok for usb connected
    for root, dirs, files in os.walk(subdirectory):
        for name in files:
            if fnmatch.fnmatch(name, '*.txt'):
                if name == 'LAEQ.txt':
                    ser3.write(Usbplug+eof)

def camera_resolution(capture_serial):
    if capture_serial==b'960':
        camera_resolution_width,camera_resolution_height=960,540
    if capture_serial==b'720':
        camera_resolution_width,camera_resolution_height=720,405
    if capture_serial==b'480':
        camera_resolution_width,camera_resolution_height=480,270
    print ("Camera resolution:",camera_resolution_width,camera_resolution_height)
    return camera_resolution_width,camera_resolution_height

def raspberry_connection():
    return ser3.write(RP1+eof)

def video_record_start():
    print("Begin recording video")
    return ser3.write(P1+eof)

def sound_record_start():
    print("Begin recording audio")
    ser3.write(Mic+eof) #signal of recording audio

# def delete_files_start():
#     return ser3.write(pdelete+eof)

def delete_files_end():
    return ser3.write(pfinish+eof)

# def return_menu():
#     return ser3.write(page1+eof)

def export_files_start():
    print ("Begin export files")
    return ser3.write(pexport+eof)

def export_files_end(export):
    if export==False:
        print ("No usb connected")
        ser3.write(pendexport+eof)
        ser3.write(perrorexport+eof)

    if export==True:
        print ("Succes in export files")
        ser3.write(pendexport+eof)
        ser3.write(Finishexport+eof)

def export_files_error():
    print ("Error in export files")
    ser3.write(pendexport+eof)
    ser3.write(perrorexport+eof)

def convert_files_start():
    print ("Begin convert files")
    return ser3.write(pconvert+eof)

def convert_files_end():
    print("Succes in convert files")
    ser3.write(pendconvert+eof)
    ser3.write(Finishconvert+eof)

def convert_files_error():
    print ("Error in convert files")
    ser3.write(pendconvert+eof)
    ser3.write(perrorconvert+eof)

def distance_screen_ref(distance_ref):
    y = b'"%d"'%distance_ref
    if distance_ref > 0 and distance_ref <= 50:
        ser3.write(t8+y+eof)
        initial_distance=distance_ref*unit
        print ('Initial distance:',initial_distance)
        return initial_distance

def unit_system(format_serial):
    if format_serial==b'in':
        unit = inch
        print ("Imperial system", unit)
    if format_serial==b'cm':
        unit = cm
        print ("Metric system", unit)
    return unit


if __name__ == '__main__':

    config = Config()

    for v in config.global_vars:
        if os.getenv(v) is None:
            print("Global variable {} is missing. Please read carefully the manual.\n".format(v))
            exit(1)

    file_manager = FileManager(config.get_capture_home())
    screen = Screen()

    # menu (page 1)
    screen.menu()

    while True:
        page_counter = ser3.readline()

        screen.set_date(get_date())
        screen.set_time(get_time())

        while page_counter==b'page2': #page 2 /  record

            screen.clear()
            raspberry_connection() #Rpi connected

            #Reading input of screen touch nextion (waiting: start)
            while start==b'':
                start=ser3.readline() #reading serial port from the screen touch
                menu_record_hour() #Hour for the menu record

                if start==b'start':    #start process of: camera, gps and distance sensor.
                    ser.open()
                    ser2.open()
                    timestamp = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                    file_video, file_sound, file_distance, file_gps = file_manager.start(id_cicliste,timestamp)   #path of every file
                    with open(file_distance, 'a') as distance_csv: #Prepare de file csv for writing
                        distance_csv.write("time,distance\n")
                    with open(file_gps, 'a') as gps_csv:
                        gps_csv.write("time,latitude,longitude\n")

                    video_record_start() #signal of recording video
                    camera_process=Process(target = get_camera, args=(file_video,camera_resolution_width,camera_resolution_height,))
                    camera_process.start()
                    sound_record_start() #signal of recording audio
                    microphone_process=Process(target = get_microphone, args=(timestamp,file_sound))
                    microphone_process.start()
                    gps_process=Process(target = get_gps_data2, args=(file_gps,))
                    gps_process.start()

                    while record==True:
                        stop=ser3.readline()
                        menu_record_hour()
                        hour=dt.datetime.now().strftime('%H:%M:%S.%f')

                        distance=get_tfmini_data(unit,initial_distance)
                        distance_screen(distance)
                        if distance>0 and distance <= maximum_sensor_distance*unit:
                            #print(hour,distance)
                            with open(file_distance, 'a') as distance_csv:
                                distance_csv.write(hour + ',' + str(distance) +  '\n')

                        if stop==b'stop':
                            record=False
                            print("End recording video")
                            camera_process.terminate()
                            camera_process.join()
                            gps_process.terminate()
                            gps_process.join()
                            subprocess.call(['pkill arecord'],shell=True)
                            print("End recording audio")
                            microphone_process.terminate()
                            microphone_process.join()
                            start=0
                            ser.close()
                            ser2.close()
                            page_counter=b'page2'

                        if stop==b'page1':
                            record=False
                            print("End recording video - page1")
                            camera_process.terminate()
                            camera_process.join()
                            gps_process.terminate()
                            gps_process.join()
                            subprocess.call(['pkill arecord'],shell=True)
                            print("End recording audio - page1")
                            microphone_process.terminate()
                            microphone_process.join()
                            start=0
                            ser.close()
                            ser2.close()
                            page_counter=b''

                if start==b'page1':    # In/out page1
                    page_counter=b''

            #return to 0
            screen.clear()
            record=True
            start=b''

        while page_counter==b'page3': #page 3 /  setup
            #Reading input of screen touch nextion (waiting: Value)
            format_serial=ser3.readline()

            if format_serial==b'page1': #In/out page 2
                page_counter=b''

            if format_serial==b'in' or format_serial==b'cm':
                try:
                    unit=unit_system(format_serial)
                except:
                    pass
                finally:
                    pass

        while page_counter==b'page4': #page 4 /  format
            #Reading input of screen touch nextion (waiting for distance ref, camera resolution, convert or export)
            capture_serial=ser3.readline()
            usb_connected() #identifies the presence of a connected usb

            if capture_serial==b'page1': #in/out menu setup
                page_counter=b''

            if capture_serial==b'capture': #Reading distance of reference
                try:
                    ser.open()
                    distance_ref = get_tfmini_data_ref(unit)
                    initial_distance = distance_screen_ref(distance_ref)
                    ser.close()
                except:
                    pass
                finally:
                    pass

            if capture_serial==b'convert': #convert button
                convert_files_start()
                try:
                    convert_video(config)
                    convert_files_end()
                except:
                    convert_files_error()
                finally:
                    pass
                print ("End convert files")

            if capture_serial==b'export': #export button
                export_files_start()
                try:
                    export=export_files ()
                    export_files_end(export)
                except:
                    export_files_error()
                finally:
                    pass
                print ("End export files")

            if capture_serial==b'960'or capture_serial==b'720' or capture_serial==b'480': #Resolution buttons
                try:
                    camera_resolution_width,camera_resolution_height=camera_resolution(capture_serial)
                except:
                    pass
                finally:
                    pass

        while page_counter==b'page5':
            # page 5  (delete files)
            delete_serial = screen.read()

            if delete_serial == b'page1':
                page_counter = b''
            elif delete_serial == b'delete':
                screen.delete_start()
                try:
                    file_manager.delete_files()
                    screen.delete_end()
                    page_counter = b''
                    screen.menu()
                finally:
                    delete_serial = b''






