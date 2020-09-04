# sensor-application
Raspberry Pi and Python application for recording/viewing sensor data

## Overview
The goal of this project is to facilitate easy installation and data recording of various sensors for Raspberry Pi devices. 
This data is then available to the user for up-to-date and historical monitoring through a Vue.js single page application.

The inspiration for this project came majorly from home gardening I've done over the past couple of years. I intend in the future to
have some form of aquaponics system, and this can be considered a prototype of a monitoring system, with other general applications.

The project is divided into 3 main parts:
* **Sensor Controller** - Controls the sensors, recording data to a database stored on the main Pi
* **Sensor Server** - Small server to edit sensor settings on secondary Pis
* **Client** - Displays current sensor readings, past readings (currently only numerical sensor information is stored, so these are
in the form of line charts), and allows the user to edit sensor settings

## Supported Sensors ##
As of right now, the project is compatible with:
* [AM2302](https://www.adafruit.com/product/393) (Adafruit)
* [BME280](https://www.waveshare.com/wiki/BME280_Environmental_Sensor) (Waveshare)

Other manufacturer's models make work as well, but I haven't tested any others yet. Both sensors record humidity and temperature. There is
a base Sensor class, with each different sensor model having its own subclass. Adding a new model class requires writing just an init method, and
a method for reading the data from the sensor.

## Future ##

* General code maintenance and polishing features. This is the second Vue project I've done, so I'm solidifying old concepts and picking up/trying out new ones.
* I have a [CO2 sensor](https://www.keyestudio.com/keyestudio-ccs811-carbon-dioxide-temperature-air-quality-sensor-for-arduino-p0581.html)
that I am hoping to get working with the project as well, but as it is meant for the Arduino I will have to write my own driver for it. After that I will
add support for other sensors as the need arises, preferably expanding to new information types sooner rather than later
* There are limitations to the Pi that can make interfacing with on-board devices difficult. For instance, the AM2302 has a analog digital converter
built in to make reading data simpler. If there is significant disruption to the ADC process, the reading ends up getting dropped.
In its current state the project operates fine on the Raspberry Pi B+ as well as the Raspberry Pi Zero W, but considerations will be made to adding a microcontroller
(probably an arduino)

## Demo ##

I have a demo version hosted on a [VM somewhere in the clouds](http://ec2-3-129-62-182.us-east-2.compute.amazonaws.com:8080/). The data is currently real data
recorded from the basement and living room of my house and, unless I have some project or anomoly I want to record, will be pretty boring. The 'edit settings'
portion of the app is just for show, so feel free to poke and prod. If you notice any serious bugs or security flaws please let me know!
