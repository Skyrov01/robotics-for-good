#!/usr/bin/env python3
"""
Keyboard control for Adeept RaspTank robot.
Use W/A/S/D to move, SPACE to stop, Q to quit.
"""

import sys
import termios
import tty
from robot_sdk.motion.motors import Motors
from robot_sdk.feedback.leds import LEDs

m = Motors()
led = LEDs()

SPEED = 40


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


print("Control the robot with keyboard:")
print("W = Forward")
print("S = Backward")
print("A = Rotate Left")
print("D = Rotate Right")
print("SPACE = Stop")
print("Q = Quit")

try:
    while True:
        key = get_key().lower()

        if key == "w":
            print("Forward")
            led.both("green")
            m.forward(SPEED)

        elif key == "s":
            print("Backward")
            led.both("yellow")
            m.backward(SPEED)

        elif key == "a":
            print("Rotate Left")
            led.left("red")
            m.rotate_left(SPEED)

        elif key == "d":
            print("Rotate Right")
            led.right("red")
            m.rotate_right(SPEED)

        elif key == " ":
            print("Stop")
            led.off()
            m.stop()

        elif key == "q":
            print("Exiting...")
            break

finally:
    m.stop()
    led.off()
    print("Robot stopped safely.")
