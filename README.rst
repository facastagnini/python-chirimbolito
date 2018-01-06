Chirimbolito
============

.. image:: https://api.codacy.com/project/badge/Grade/09b74b48abd44905892de63270b0e77d
   :target: https://www.codacy.com/app/facastagnini_2/chirimbolito?utm_source=github.com&utm_medium=referral&utm_content=facastagnini/chirimbolito&utm_campaign=badger
.. image:: https://badge.fury.io/py/chirimbolito.svg
   :target: https://badge.fury.io/py/chirimbolito

A Bitcoin address monitoring tool built with a Raspberry Pi and a LCD display

You will need
=============

-   a Raspberry Pi
-   one micro SD card
-   the LCD screen, [Adafruit RGB Negative 16x2 LCD+Keypad Kit for Raspberry Pi](https://www.adafruit.com/product/1110)
-   one or more bitcoin address to monitor

How to build it
===============

-   Install Raspbian Stretch Lite on the micro SD card. This is beyond the scope of this document, you can find a good guide [here](https://www.raspberrypi.org/downloads/raspbian/).
-   [Enable sshd on a headless Raspberry Pi](https://www.raspberrypi.org/documentation/remote-access/ssh/)
-   Install the LCD screen and the micro SD card in the Raspberry Pi
-   Boot the Raspberry Pi
-   ssh into the Raspberry Pi and install the bitcoin address monitoring tool

        WIP
        ssh pi@raspbian
        password: (the default password is 'raspberry')
        raspbian$ mkdir chirimbolito
        raspbian$ virtualenv chirimbolito
        raspbian$ cd chirimbolito
        raspbian$ source bin/activate
        raspbian$ pip install chirimbolito

-   Edit the file `configuration.json` to configure the bitcoin addresses that you want to monitor.
