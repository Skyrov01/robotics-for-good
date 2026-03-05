"""
    This example demonstrates how to control the arm of the robot using the Arm class from the robot_sdk. 
    It shows how to move the base, shoulder, elbow, and hand (gripper) to different positions. 
    The arm will always reset to the home position when initialized.
"""
import time
from robot_sdk.arm.arm import Arm

# Always resets to home position when initialized
arm = Arm()

arm.home()
# Control the gripper: -20 to 20

while True:
    arm.hand(20)
    time.sleep(1)
    arm.hand(-20)
    time.sleep(1)

