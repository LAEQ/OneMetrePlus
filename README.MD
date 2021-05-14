# Capture Raspberry Pi project

Raspberry project for recording traffic during a bike ride.


## Configuration
Some global environments are required to run the project. Please add the following variables to your environement.

```bash
# ~/.bashrc
export PROJECT_HOME=/home/pi/path/to/clone/project
export CAPTURE_HOME=/home/pi/path/where/to/save/files
export PYTHONPATH=$PYTHONPATH:$PROJECT_HOME
```


#### Systemd service  

To start the program after login, we use systemd to managed the python main script.

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