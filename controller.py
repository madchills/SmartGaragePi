#Software to monitor and control garage doors via a raspberry pi

import time, uuid, os
import smtplib
import RPi.GPIO as gpio
import yaml
import httplib
import urllib
import subprocess

from flask import Flask

config_path = os.getcwd() + "/config.yaml"
with open(config_path, 'r') as stream:
    config = yaml.safe_load(stream)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
