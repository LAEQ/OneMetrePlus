# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 10:06:28 2019

@author: GelbJ

Modifié par: AndresH
"""

#Code pour exporter les videos en format mp4

import subprocess
import sys
import os
from path import Path
#sys.path.append("I:/Python/_____GitProjects/BruteMP")
#from BruteMP import MPWorker
#from PathLib import Path

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

#####################
#Generer les commandes
#####################

#ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac output.mp4

Videos = InPutFolder.walkfiles("*.h264")
Commandes = []
BaseCommande = 'ffmpeg -r 24 -i "++Inputvideo++" -i "++Inputsound++" -c:v copy -c:a aac -r 24 "++Output++"'
for Video in Videos :
    print ("Begin convert")
    Inputvideo = Video
    Inputsound = InputSoundFolder.joinpath(Video.name)
    Output = OutPutFinalFolder.joinpath(Video.name)
    print(Inputvideo)
    print(Inputsound)
    print(Output)
    thisCommande = BaseCommande.replace("++Inputvideo++",Inputvideo.replace("\\","/")).replace("++Inputsound++",Inputsound.replace(".h264",".wav")).replace("++Output++",Output.replace(".h264",".mp4"))
    print("Executing this command : "+thisCommande)
    os.system(thisCommande)
    print ("End convert")

      






