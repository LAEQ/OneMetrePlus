#!/bin/bash


ici=$(pwd)

scp -r pi@192.168.1.16:/home/pi/captures/* $ici/captures
