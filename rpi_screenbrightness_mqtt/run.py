# Copyright 2019 bitconnect
# Author: Tobias Perschon
# License: GNU GPLv3, see LICENSE

import configparser,sys, time
import paho.mqtt.client as mqtt
from rpi_backlight import Backlight

class rpiSBmqtt:

    def __init__(self, config_path):
        # Load the configuration.
        self._config = configparser.ConfigParser()
        if len(self._config.read(config_path)) == 0:
            raise RuntimeError(
                'Failed to find configuration file at {0}, is the application properly installed?'.format(config_path))
        self._mqttbroker = self._config.get('mqtt', 'broker')
        self._mqttuser = self._config.get('mqtt', 'user')
        self._mqttpassword = self._config.get('mqtt', 'password')
        self._mqttconnectedflag = False
        self._mqtt_state_topic = self._config.get('mqtt', 'state_topic')
        self._mqtt_command_topic = self._config.get('mqtt', 'command_topic')
        self._mqtt_brightness_state_topic = self._config.get('mqtt', 'brightness_state_topic')
        self._mqtt_brightness_command_topic = self._config.get('mqtt', 'brightness_command_topic')
        self._mqtt_clientid = self._config.get('mqtt', 'clientid')
        self._console_output = self._config.getboolean('misc', 'debug')

        # initalise backlight object
        try:
            self._backlight = Backlight()
            self._backlight.fade_duration = self._config.getfloat('backlight', 'fade_duration')
        except:
            self._print("Could not initialise backlight component. Are you running this on a RPi?")
            exit(1)

    def _print(self, message):
        """Print message to standard output if console output is enabled."""
        if self._console_output:
            print(message)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._print("Connected!")
            self._mqttconnectedflag = True
            client.subscribe(self._mqtt_brightness_command_topic)
            client.subscribe(self._mqtt_command_topic)
        else:
            self._mqttconnectedflag = False
            self._print("Could not connect. Return code: " + str(rc))

    def on_message(self, client, userdata, msg):
        payload = str(msg.payload.decode("utf-8"))
        topic = msg.topic

        if topic == self._mqtt_command_topic:
            self._print("power: "+str(payload))
            self._backlight.power = True if payload == "ON" else False
            self.sendStatus(client)

        if topic == self._mqtt_brightness_command_topic:
            self._print("brightness: "+str(payload))
            self._backlight.brightness = int(payload)
            self.sendStatus(client)

    def on_disconnect(self, client, userdata, rc):
        self._print("disconnected. reason:  " + str(rc))
        self._mqttconnectedflag = False

    def sendStatus(self, client):
        payload_brightness = str(self._backlight.brightness)
        payload_power = "ON" if self._backlight.power else "OFF"
        self._print("Publishing " + payload_brightness + " to topic: " + self._mqtt_brightness_state_topic + " ...")
        client.publish(self._mqtt_brightness_state_topic, payload_brightness, 0, False)
        self._print("Publishing " + payload_power + " to topic: " + self._mqtt_state_topic + " ...")
        client.publish(self._mqtt_state_topic, payload_power, 0, False)

    def run(self):
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,self._mqtt_clientid)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect
        client.username_pw_set(self._mqttuser, self._mqttpassword)
        self._print("Connecting to broker "+self._mqttbroker)
        client.loop_start()
        try:
            client.connect(self._mqttbroker, 1883, 60)
        except:
            self._print("Connection failed!")
            exit(1)

        while not self._mqttconnectedflag:  # wait in loop
            self._print("Waiting for connection...")
            time.sleep(1)
        while self._mqttconnectedflag:
            try:
                self.sendStatus(client)
            except Exception as e:
                self._print("exception")
                self._print(str(e))

            time.sleep(10)

        client.loop_stop()  # Stop loop
        client.disconnect()  # disconnect


# Main entry point.
if __name__ == '__main__':
    print('Starting rpi (touch)screen brightness control via mqtt.')
    config_path = '/etc/rpi_screenbrightness_mqtt.conf'
    # Override config path if provided as parameter.
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
    rpiControl = rpiSBmqtt(config_path)
    rpiControl.run()
