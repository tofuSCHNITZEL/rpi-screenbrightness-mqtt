#!/bin/bash

set -e
cd "$(dirname "$0")"


# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root. Try: sudo ./install.sh"
  exit 1
fi


echo "Installing dependencies..."
echo "=========================="
apt update && apt -y install python3 python3-pip git

python3 -m pip install .

cp ./assets/rpi_screenbrightness_mqtt.conf /etc/rpi_screenbrightness_mqtt.conf


echo "Configuring service to run on start..."
echo "==========================================="

cp ./assets/rpi_screenbrightness_mqtt.service /etc/systemd/system/rpi_screenbrightness_mqtt.service
chmod 644 /etc/systemd/system/rpi_screenbrightness_mqtt.service

systemctl daemon-reload
systemctl enable rpi_screenbrightness_mqtt.service
systemctl start rpi_screenbrightness_mqtt.service
sleep 1
systemctl status rpi_screenbrightness_mqtt.service

echo "Install finished! If service status above in not active, please troubleshoot"