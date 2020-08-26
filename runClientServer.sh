#!/bin/bash
cd /home/pi/sensor-application
export FLASK_APP=clientServer.py
flask run --host 0.0.0.0
