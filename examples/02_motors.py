"""
    This example demonstrates how to control the motors of the robot using the Motors class from the robot_sdk. 
    It shows how to move forward, rotate left and right, and move backward while providing visual feedback using the LEDs.
"""

from robot_sdk.motion.motors import Motors
from robot_sdk.feedback.leds import LEDs

import time

led = LEDs()

m = Motors()

try:
    print("Forward")
    led.both("green")
    m.forward(40)
    time.sleep(2)

    print("Rotate left")
    led.left("red")
    m.rotate_left(40)
    time.sleep(1)

    led.off()

    print("Rotate right")
    led.right("red")
    m.rotate_right(40)
    time.sleep(1)

    led.off()

    print("Backward")
    led.both("yellow")
    m.backward(40)
    time.sleep(2)

finally:
    m.stop()
    led.off()
