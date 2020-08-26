#!/bin/bash
cd /home/pi/sensor-application
export FLASK_APP=sensorServer.py
flask run --host 0.0.0.0 --port 5001
