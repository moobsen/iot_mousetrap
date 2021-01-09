#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Copyright {2021} {Bluebird Mountain | Moritz Obermeier}

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import RPi.GPIO as GPIO
import time
import datetime
import subprocess

def setup_GPIO(MOUSETRAP_PIN ):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(MOUSETRAP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main():
  MOUSETRAP_PIN = 2
  setup_GPIO(MOUSETRAP_PIN)
  mail_was_sent = 0

  while True:
    f = open("mouse-status.txt", "w+")
    if (GPIO.input(MOUSETRAP_PIN) == 0):
      print(datetime.datetime.now(), "<p> EEEEK!! MOUSE!!", file=f)
      if (mail_was_sent == 0):
        subprocess.run(['python3', '/home/pi/src/mousetrap/send_status_smtp.py'])
        mail_was_sent = 1
      else:
        print("<p> Mail has been sent!", file=f)
    else:
      print(datetime.datetime.now(), "<p> Chill. No mouse.", file=f)
      mail_was_sent = 0
    f.close()
    time.sleep(2)
    open("mouse-status.txt", "w").close()

  #we should never get here...
  sys.exit(0)   

if __name__ == "__main__": 
  main()
