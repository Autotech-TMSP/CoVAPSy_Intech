#!/bin/bash

# Configure the Ethernet interface with a static IP address for the lidar
sudo sh -c 'echo "[Match]" > /etc/systemd/network/eth0.network'
sudo sh -c 'echo "Name=eth0" >> /etc/systemd/network/eth0.network'
sudo sh -c 'echo "[Network]" >> /etc/systemd/network/eth0.network'
sudo sh -c 'echo "Address=192.168.0.20/24" >> /etc/systemd/network/eth0.network'

# Enable and start the systemd-networkd service. Allowing the Ethernet interface to be configured with the static IP address
sudo systemctl enable systemd-networkd
sudo systemctl start systemd-networkd
sudo systemctl restart systemd-networkd

# Add the PWM overlay configuration to the boot config file
sudo sh -c 'echo "dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4" >> /boot/firmware/config.txt'

# Install necessary Python packages within the virtual environment
pip install Adafruit-SSD1306 --break-system-packages
pip install rpi_hardware_pwm --break-system-packages
pip install matplotlib --break-system-packages
pip install RPi.GPIO --break-system-packages
pip install numpy --break-system-packages 
pip install onnx --break-system-packages


# Add the cron job to run the script at reboot
(crontab -l 2>/dev/null; echo "@reboot /home/intech/CoVAPSy/scripts/startup.sh") | crontab -

