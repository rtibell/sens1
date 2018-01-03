#!/bin/bash
scp *.py pi@192.168.0.19:/home/pi/Projects/sens1/
scp html/* pi@192.168.0.19:/var/www/html
scp IOT-cert/* pi@192.168.0.19:/home/pi/Projects/sens1/IOT-cert
