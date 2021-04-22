# Capture Raspberry Pi 

#### Test unitaires
```bash
python3 -m unittest
```

#### Configuration service  
Create a file ~/.config/systemd/user/capture.service

```
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
# Create log files (mandatory)
touch /home/pi/info.log /home/pi/error.log
systemctl --user daemon-reload
systemctl --user enable capture.service
systemctl --user start capture.service
```

#### Manage services 

```bash
systemctl start|stop capture
systemctl enable|disable capture
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

### Wifi card
```bash
ip link set dev eth0 down
```