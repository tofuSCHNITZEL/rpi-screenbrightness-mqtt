from setuptools import setup, find_packages

setup(
    name              = 'rpi_screenbrightness_mqtt',
    version           = '0.6.0',
    author            = 'Tobias Perschon',
    author_email      = 'tobias@perschon.at',
    description       = 'A simple service that conntects to an mqtt broker so you can control the backlight of an rpi (touch)screen via mqtt (and eg. homeassistant)',
    license           = 'GNU GPLv3',
    url               = 'https://github.com/tofuSCHNITZEL/rpi-screenbrightness-mqtt',
    install_requires  = ['rpi-backlight', 'paho-mqtt'],
    packages          = find_packages()
)
