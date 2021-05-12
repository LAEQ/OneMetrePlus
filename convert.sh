#!/usr/bin/bash


for videoFile in captures/video/*;
do
    soundFile=$(echo $videoFile | sed "s/video/sound/" | sed "s/h264/wav/")
    targetFile1=$(echo $videoFile | sed "s/video/export/" | sed "s/h264/_1.mp4/")
    targetFile2=$(echo $videoFile | sed "s/video/export/" | sed "s/h264/_2.mp4/")


    echo converting $videoFile
    
    # basic
    ffmpeg -r 24 -i $videoFile -i $soundFile  -c:v copy -c:a aac -r 24 $targetFile1

    # 
    ffmpeg -i $videoFile -i $soundFile  -c:v copy -c:a aac -shortest $targetFile2

done


# rm version_*.mp4

# # basic
# ffmpeg -r 24 -i video/ID1_C1_2021_04_21_12_50_40.h264 -i sound/ID1_C1_2021_04_21_12_50_40.wav  -c:v copy -c:a aac -r 24 version_0.mp4

# # 
# ffmpeg -i video/ID1_C1_2021_04_21_12_50_40.h264 -i sound/ID1_C1_2021_04_21_12_50_40.wav  -c:v copy -c:a aac -shortest version_1.mp4
