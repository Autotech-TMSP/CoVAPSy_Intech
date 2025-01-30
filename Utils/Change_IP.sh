# Configure the Ethernet interface with a static IP address
sudo sh -c 'echo "[Match]" > /etc/systemd/network/eth0.network'
sudo sh -c 'echo "Name=eth0" >> /etc/systemd/network/eth0.network'
sudo sh -c 'echo "[Network]" >> /etc/systemd/network/eth0.network'
sudo sh -c 'echo "Address=192.168.0.20/24" >> /etc/systemd/network/eth0.network'

# Enable and start the systemd-networkd service
sudo systemctl enable systemd-networkd
sudo systemctl start systemd-networkd
sudo systemctl restart systemd-networkd

# Install necessary Python packages
sudo apt-get install python3-matplotlib
sudo apt-get install python3-rpi.gpio
pip install Adafruit-SSD1306 --break-system-package

# Install the rpi_hardware_pwm package, bypassing the system package management
pip install rpi_hardware_pwm --break-system-package

# Add the PWM overlay configuration to the boot config file
sudo sh -c 'echo "dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4" >> /boot/firmware/config.txt'