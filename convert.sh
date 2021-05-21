#!/usr/bin/bash


for videoFile in captures/video/*;
do
    soundFile=$(echo $videoFile | sed "s/video/sound/" | sed "s/h264/wav/")
    targetFile0=$(echo $videoFile | sed "s/video/export/" | sed "s/.h264/_0.mp4/")
    targetFile1=$(echo $videoFile | sed "s/video/export/" | sed "s/.h264/_1.mp4/")
    targetFile2=$(echo $videoFile | sed "s/video/export/" | sed "s/.h264/_2.mp4/")
    targetFile3=$(echo $videoFile | sed "s/video/export/" | sed "s/.h264/_3.mp4/")
    boxFile="captures/export/video_box.mp4"

    echo converting $videoFile

    ffmpeg -y -r 25 -i $videoFile -i $soundFile -c:v copy -c:a aac $targetFile0
    ffmpeg -y -re -vsync 1 -async 1 -i $videoFile -i $soundFile -c:v copy -c:a aac -shortest $targetFile1
    ffmpeg -y  -i  $videoFile -i $soundFile  -c:v copy -c:a aac -shortest $targetFile2
    ffmpeg -y -vsync 1 -async 25 -i $videoFile -i $soundFile -c:v copy -c:a aac -shortest $targetFile3

    MP4Box -add $videoFile $boxFile


    ffprobe -loglevel error -select_streams a:0 -show_entries packet=pts_time,duration -of csv=print_section=0 $soundFile > "captures/export/sound_frames.csv"
    ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,duration -of csv=print_section=0 $videoFile > "captures/export/video_frames_h264.csv"
    ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,duration -of csv=print_section=0 $boxFile > "captures/export/video_box.csv"

    ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,duration -of csv=print_section=0 $targetFile1 > "captures/export/video_frames_1_v:0.csv"
    ffprobe -loglevel error -select_streams a:0 -show_entries packet=pts_time,duration -of csv=print_section=0 $targetFile1 > "captures/export/video_frames_1_a:0.csv"

    cut -d '.' -f 1 "captures/export/video_frames_1_v:0.csv" | uniq -c > "captures/export/video_sum"
    cut -d '.' -f 1 "captures/export/video_frames_1_a:0.csv" | uniq -c > "captures/export/sound_sum"

    echo "captures/export/video_sum"
    cat "captures/export/video_sum" | tr -d ' ' | cut -c 1-2 | sort | uniq -c

    echo "captures/export/sound_sum"
    cat "captures/export/sound_sum" | tr -d ' ' | cut -c 1-2 | sort | uniq -c

done


# rm version_*.mp4

# # basic
# ffmpeg -r 24 -i video/ID1_C1_2021_04_21_12_50_40.h264 -i sound/ID1_C1_2021_04_21_12_50_40.wav  -c:v copy -c:a aac -r 24 version_0.mp4

# #
# ffmpeg -i video/ID1_C1_2021_04_21_12_50_40.h264 -i sound/ID1_C1_2021_04_21_12_50_40.wav  -c:v copy -c:a aac -shortest version_1.mp4

#ffprobe -loglevel error -select_streams a:0 -show_entries packet=pts_time,flags -of csv=print_section=0 captures/sound/video.wav | awk -F',' '/K/ {print $1}'

#ffprobe -loglevel error -show_streams captures/sound/video.wav

# ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,flags -of csv=print_section=0 input.mp4