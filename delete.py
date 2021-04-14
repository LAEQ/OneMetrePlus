# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 10:06:28 2019

@author: AndresH
"""

#Code pour eliminer les fichiers 

import sys
import os
from path import Path

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