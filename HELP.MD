#Git
```bash
# Setup
git clone <url>
git checkout -b <name>

# Workflow
git status
git add filename #add a file to a commit
git rm filename #remove a file to a commit
git commit -m 'Commit message'
git push origin <branch_name>
git pull origin <branch_name>

# Misc
git log
git fetch 
```

# Config
Username pi
password Inrs2020

https://stackoverflow.com/questions/17553543/pyserial-non-blocking-read-loop
https://docs.python.org/2/library/multiprocessing.html
http://www.voxforge.org/home/docs/faq/faq/linux-how-to-determine-your-audio-cards-or-usb-mics-maximum-sampling-rate
https://tinkering.xyz/async-serial/
https://blog.miguelgrinberg.com/post/how-to-make-python-wait
https://cuyu.github.io/python/2016/08/15/Terminate-multiprocess-in-Python-correctly-and-gracefully
https://www.infoworld.com/article/3315121/python-threading-and-subprocesses-explained.html

https://opensource.com/article/17/6/ffmpeg-convert-media-file-formats
https://ostechnix.com/20-ffmpeg-commands-beginners/

```
# print or control the kernel ring buffer
dmesg
```

```
# Get number of frames
ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 test.h264

# Get duration
ffmpeg -i test.h264 -f null -

```