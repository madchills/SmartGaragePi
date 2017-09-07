# SmartGaragePi
=================
Monitor and control your garage doors from the web via a raspberry Pi.

Overview:
---------

This project provides software and hardware installation instructions for monitoring and controlling your garage doors remotely (via a browser or Rest). The software is designed to run on a [Raspberry Pi](www.raspberrypi.org), which is an inexpensive ARM-based computer

Requirements:
-------------

Although you can buy a [Raspbery Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/), that is definetly overkill for this project.  If you have any of the hardware below, I would recommend buying version 1 or 2

**Hardware**
* [Raspberry Pi](http://www.raspberrypi.org)
* Micro USB charger (1.5A preferable)
* [USB WiFi dongle](http://amzn.com/B003MTTJOY) (If connecting wirelessly)
* 8 GB micro SD Card
* Relay Module, 1 channel per garage door (I used [SainSmart](http://amzn.com/B0057OC6D8 ), but there are [other options](http://amzn.com/B00DIMGFHY) as well)
* [Magnetic Contact Switch](http://amzn.com/B006VK6YLC) (one per garage door)
* [Female-to-Female jumper wires](http://amzn.com/B007XPSVMY) (you'll need around 10, or you can just solder)
* 2-conductor electrical wire

**Software**

* [Raspbian](http://www.raspbian.org/)
* Python >2.7 (installed with Raspbian)
* Raspberry Pi GPIO Python libs (installed with Raspbian)
* [Flask](http://flask.pocoo.org/)

Hardware Setup:
---------------

*Step 1: Install the magnetic contact switches:*

Software Installation:
-----

1. **Install [Raspbian](http://www.raspbian.org/) onto your Raspberry Pi**
    1. [Tutorial](http://www.raspberrypi.org/wp-content/uploads/2012/12/quick-start-guide-v1.1.pdf)
    2. [Another tutorial](http://www.andrewmunsell.com/blog/getting-started-raspberry-pi-install-raspbian)
    3.  [And a video](http://www.youtube.com/watch?v=aTQjuDfEGWc)!

2. **Configure your WiFi adapter** (if necessary).
    
    - [Follow this tutorial](http://www.frodebang.com/post/how-to-install-the-edimax-ew-7811un-wifi-adapter-on-the-raspberry-pi)
    - [or this one](http://www.youtube.com/watch?v=oGbDawnqbP4)

    *From here, you'll need to be logged into your RPi (e.g., via SSH).*

3. **Install the python twisted module** (used to stand up the web server):

    `sudo apt-get install python-twisted`
    
4. **Install the controller application**