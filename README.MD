# Capture Raspberry Pi

#### Configuration service  
Create a file ~/.config/systemd/user/capture.service

Note: modify the user accordingly !

```
[Unit]
Description=Capture service
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 script.py
StandardOutput=append:/home/pi/info.log
StandardError=append:/home/pi/error.log

Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target

[Install]
WantedBy=multi-user.target
Alias=capture.service
```

Configuration
```bash
# Create log files (mandatory)
touch /home/david/info.log /home/david/error.log
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

#### List of services to stop & disable
- cups
- bluetooth
- cron 
- 

### Wifi card
```bash
ip link set dev eth0 down
```
