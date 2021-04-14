# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 10:06:28 2019

@author: 
"""
import subprocess
import sys
import os
import glob
from path import Path
import fnmatch


InPutFolder = Path("/home/pi/Desktop/Capteur/files")
subdirectory = "/media/pi/"

#if we need find it first
#print (InPutFolder)

for root, dirs, files in os.walk(subdirectory):
    for name in files:
        if fnmatch.fnmatch(name, '*.txt'):
            if name == 'LAEQ.txt':
                print("Begin exportation") 
                Subfolder = root
                OutPutFolder = Path(Subfolder)
                print(InPutFolder,OutPutFolder)
                #subprocess.run('cp -r '+ InPutFolder +' '+ OutPutFolder, shell=True) 
                os.system('cp -r '+ InPutFolder +' '+ OutPutFolder)
                print (os.path.join(root, name))
                os.system('umount '+OutPutFolder)
                #os.system('eject '+OutPutFolder)
                #print (root)
                print("End exportation") 
            else:
                print ('Error exportation, no usb')








