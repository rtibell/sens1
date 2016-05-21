#!/usr/bin/python

from flask import render_template
from flask import Flask
from sense_hat import SenseHat

app = Flask(__name__)

@app.route('/')
def root():
    sense = SenseHat()
    temp1 = sense.get_temperature()   
    temp2 = sense.get_temperature_from_pressure() 
    pressure = sense.get_pressure()
    north = sense.get_compass()
    accel_only = sense.get_accelerometer()
    acc_raw = sense.get_accelerometer_raw()
    temp = "Temp {:10.4f}".format(temp1) + " {:10.4f}".format(temp2) 
    other = "Pres {:10.4f}".format(pressure) + " Compas {:10.4f}".format(north)
    acc1 = "p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only)
    acc2 = "x: {x}, y: {x}, z: {z}".format(**acc_raw)
    return temp + "\n" + other + "\n" + acc1 + "\n" + acc2 + "\n"

@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    sense = SenseHat()
    sense.show_message("Hello world!")
    return render_template('index.html',
                           title='Home',
                           user=user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
