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
apt update && apt -y install python3 python3-pip git supervisor

pip3 install setuptools
python3 setup.py install --force

cp ./assets/rpi_screenbrightness_mqtt.conf /etc/rpi_screenbrightness_mqtt.conf


echo "Configuring service to run on start..."
echo "==========================================="

cp ./assets/rpi_screenbrightness_mqtt_service.conf /etc/supervisor/conf.d/rpi_screenbrightness_mqtt_service.conf

service supervisor restart


echo "Finished!"