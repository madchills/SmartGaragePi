#Software to monitor and control garage doors via a raspberry pi

import os, syslog, time, uuid
import smtplib
import RPi.GPIO as gpio
import yaml
import httplib
import urllib
import subprocess

from flask import Flask, render_template

config_path = os.getcwd() + "/config.yaml"
with open(config_path, 'r') as stream:
    config = yaml.safe_load(stream)

config['door']['last_action'] = None
config['door']['last_action_time'] = None
config['door']['current_status'] = None

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)
gpio.setup(config['door']['relay_pin'], gpio.OUT)
gpio.setup(config['door']['state_pin'], gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.output(config['door']['relay_pin'], True)

app = Flask(__name__)

@app.route('/')
def home_page():
    user = config['config']['user']
    name = config['door']['name']
    status = get_door_status()
    cdate= 'RIGHT NOW!' #change this
    return render_template('index.html', user=user, name=name, status=status, cdate=cdate)

@app.route('/status')
def get_door_status():
    if gpio.input(config['door']['state_pin']) == config['door']['state_pin_closed_value']:
        return 'closed'
    elif config['door']['last_action'] == 'open':
        if time.time() - config['door']['last_action_time'] >= config['door'].get('approx_time_to_open', 10):
            return 'open'
        else:
            return 'opening'
    elif config['door']['last_action'] == 'close':
        if time.time() - config['door']['last_action_time'] >= config['door'].get('approx_time_to_close', 10):
            return 'open' #This state indicates a problem
        else:
            return 'closing'
    else:
        return 'open'

@app.route('/toggle')
def toggle_relay():
    state = get_door_status()
    if (state == 'open'):
        config['door']['last_action'] = 'close'
        config['door']['last_action_time'] = time.time()
    elif (state == 'closed'):
        config['door']['last_action'] = 'open'
        config['door']['last_action_time'] = time.time()
    else:
        config['door']['last_action'] = None
        config['door']['last_action_time'] = None

    gpio.output(config['door']['relay_pin'], False)
    time.sleep(0.2)
    gpio.output(config['door']['relay_pin'], True)
    if config['door']['last_action'] == 'close':
        return 'closing'
    if config['door']['last_action'] == 'open':
        return 'opening'


if __name__ == '__main__':
    app.run(port=config['site']['port'], host=config['site']['access'])

