# Capture Raspberry Pi

#### Configuration service  
Create a file ~/.config/systemd/user/capture.service

Note: modify accordingly with your setup !

```bash
[Unit]
Description=Capture service

[Service]
Type=simple
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 script.py
StandardOutput=append:/home/pi/info.log
StandardError=append:/home/pi/error.log

Restart=always
RestartSec=1

[Install]
WantedBy=default.target
Alias=capture.service
```

Configuration
```bash
# Create log files (mandatory)
touch /home/pi/info.log /home/pi/error.log
systemctl --user daemon-reload
systemctl --user enable capture.service
systemctl --user start capture.service
```

#### Manage services 

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
