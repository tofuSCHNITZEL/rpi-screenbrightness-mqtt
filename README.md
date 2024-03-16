# rpi-screenbrightness-mqtt

This service can be used to control the backlight of a raspberrypi (touchscreen) e.g. the official 7" touchsceen via mqtt.   
The default config works with homeassistant if used with the config example for home assistant below. (You just have
to enter your mqtt broker info)  
The project uses the systemd package, so it will run automatically on startup and restart upon error. The script publishes the current 
state of power and brightness every 10 seconds.

## How to install:

1. clone this repository to your raspberry pi  
`git clone https://github.com/tofuSCHNITZEL/rpi-screenbrightness-mqtt`
2. run installer  
`sudo ./rpi-screenbrightness-mqtt/install.sh`
3. edit config and enter your mqtt broker info and optional change the control and state topics  you can use "${HOSTNAME}" in clientid, state_topic, command_topic, brightness_state_topic, brightness_command_topic and it will be replaced by the hostname of the device
`sudo nano /etc/rpi_screenbrightness_mqtt.conf`


## Trouble shooting
* to enable debug output set "debug" to True or 1 in `/etc/rpi_screenbrightness_mqtt.conf`  
you can find the logs via `sudo journalctl -u rpi_screenbrightness_mqtt.service'
* you can check the status with `sudo systemctl status rpi_screenbrightness_mqtt` or 
restart the service with ` sudo systemctl restart rpi_screenbrightness_mqtt` 

### Home Assistant config example

to enable control of the backlight via a homeassistant light use the following configuration:

~~~~
light:
  - platform: mqtt
    name: "dashboard backlight"
    state_topic: "stat/rpi1/power"
    command_topic: "cmnd/rpi1/power"
    brightness_state_topic: "stat/rpi1/brightness"
    brightness_command_topic: "cmnd/rpi1/brightness"
    brightness_scale: 100
~~~~