# One Metre Plus (1m+)

A multifunctional open source sensor for bicycles based on raspberry pi.

<a href="https://github.com/LAEQ/OneMetrePlus/blob/master/ressources/Logo_One_Meter_Plus.png"><img src="https://github.com/LAEQ/OneMetrePlus/blob/master/ressources/Logo_One_Meter_Plus.png" width="400"/>
  <a href="https://github.com/LAEQ/OneMetrePlus/blob/master/ressources/Plan_One_metre_plus.png">
  <img src="https://github.com/LAEQ/OneMetrePlus/blob/master/ressources/Plan_One_metre_plus.png" width="350"/>
<a href="https://github.com/LAEQ/OneMetrePlus/blob/master/ressources/Schema.png">
  <img src="https://github.com/LAEQ/OneMetrePlus/blob/master/ressources/Schema.png" width="800"/>
  
## Our recommendation
### Systemd service  

To start the program after login, we use systemd to manage the python main script.

You must create a file with the following configuration accordingly with your setup. 

| IMPORTANT: The log files must be created before the start/enabling of the service. The service does not generate the files.
```bash
# ~/.config/systemd/user/capture.service
[Unit]
Description=Capture service

[Service]
Type=simple
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 main.py
StandardOutput=append:/home/pi/info.log
StandardError=append:/home/pi/error.log

Restart=always
RestartSec=1

[Install]
WantedBy=default.target
Alias=capture.service
```

Configuration logs
```bash
systemctl --user daemon-reload
systemctl --user enable capture.service
systemctl --user start capture.service
```

### Some services to disable 

```bash
systemctl start|stop service
systemctl enable|disable service
systemctl list-units --type=service

#Example: Stop bluetooth
systemctl status bluetooth.service
systemctl stop bluetooth.service
systemctl disable bluetooth.service

# Disable wifi, bluetooth
systemctl disable wpa_supplicant
systemctl disable bluetooth
systemctl disable hciuart
```

#### List of services to stop & disable
- cups & cups-browsed
- bluetooth
- cron 

### Wifi card
```bash
ip link set dev eth0 down
```

#### Unit tests
```bash
python3 -m unittest discover
```

#### Configuration .nanobashrc
```bash
export PROJECT_HOME=/home/pi/capteur-henao
export CAPTURE_HOME=/home/pi/captures
export PYTHONPATH=$PYTHONPATH:$PROJECT_HOME
```
  
  ## Required libraries

| # | version |
| --- | --- |
| pyserial  | 3.5 |
| multiprocess  | 0.70.11.1|
| path  | 15.1.2 |
| pynmea2  | 1.18.0 | 
| PyYAML  | 5.4.1 |
  
##Software License

##3D Model License
<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />The 3D model of One Metre Plus is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
