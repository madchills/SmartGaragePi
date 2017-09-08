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

for door in config['doors']:
    config['doors'][door]['last_action'] = None
    config['doors'][door]['last_action_time'] = None
    config['doors'][door]['current_status'] = None

gpio.setmode(gpio.BCM)
gpio.setup()

app = Flask(__name__)

@app.route('/')
def home_page():
    user = config['config']['user']
    name = config['doors']['only']['name']
    return render_template('index.html', user=user, name=name)


def uptime(seconds, suffixes=['y','w','d','h','m','s'], add_s=False, separator=' '):
    """
    Takes an amount of seconds and turns it into a human-readable amount of time.
    """
    # the formatted time string to be returned
    time = []

    # the pieces of time to iterate over (days, hours, minutes, etc)
    # - the first piece in each tuple is the suffix (d, h, w)
    # - the second piece is the length in seconds (a day is 60s * 60m * 24h)
    parts = [(suffixes[0], 60 * 60 * 24 * 7 * 52),
             (suffixes[1], 60 * 60 * 24 * 7),
             (suffixes[2], 60 * 60 * 24),
             (suffixes[3], 60 * 60),
             (suffixes[4], 60),
             (suffixes[5], 1)]

    # for each time piece, grab the value and remaining seconds, and add it to
    # the time string
    for suffix, length in parts:
        value = seconds / length
        if value > 0:
            seconds = seconds % length
            time.append('%s%s' % (str(value),
                                  (suffix, (suffix, suffix + 's')[value > 1])[add_s]))
        if seconds < 1:
            break

    return separator.join(time)

def get_door_status(door):
    if gpio.input(config['doors'][door]['state_pin']) == config['doors'][door]['state_pin_closed']
        return 'closed'
    elif config['doors'][door]['last_action'] == 'open':
        if time.time() - config['doors'][door]['last_action_time] >= config['doors'][door].get('approx_time_to_open', 10):
            return 'open'
        else:
            return 'opening'
    elif self.last_action == 'close'
        if time.time() - config['doors'][door]['last_action_time] >= config['doors'][door].get('approx_time_to_close', 10):
            return 'open' #This state indicates a problem
        else:
            return 'closing'
    else:
        return 'open'

def toggle_relay(door):
    state = get_door_status(door)
    if (state == 'open'):
        config['doors'][door]['last'action] = 'close'
        config['doors'][door]['last_action_time'] = time.time()
    if (state == 'closed'):
        config['doors'][door]['last'action] = 'open'
        config['doors'][door]['last_action_time'] = time.time()
    else:
        config['doors'][door]['last'action] = None
        config['doors'][door]['last_action_time'] = None

    gpio.output(config['doors'][door]['relay_pin'], False)
    time.sleep(0.2)
    gpio.output(config['doors'][door]['relay_pin'], True)


if __name__ == '__main__':
    app.run()

