"""
Robotics for Good – LED Example
-------------------------------

This program demonstrates how to use the robot LED system
to communicate robot state and direction.

LED MEANING:
- Green  : robot ready
- Blue   : idle / waiting
- Yellow : turning
- Red    : alert
"""

from robot_sdk.feedback.leds import LEDs
import time


led = LEDs()

print("Robot starting up")
led.both("green")          # Robot ready
time.sleep(2)

print("Idle mode")
led.both("blue")
time.sleep(2)

print("Turning left")
led.turn_signal("left")
time.sleep(1)

led.both("blue")

print("Turning right")
led.turn_signal("right")
time.sleep(1)

print("Warning / alert mode")
led.police()
time.sleep(4)

print("Shutting down LEDs")
led.off()


