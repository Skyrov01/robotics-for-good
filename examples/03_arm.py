import time
from robot_sdk.arm.arm import Arm

# Always resets to home position when initialized
arm = Arm()



try:
    # Control the gripper: -20 to 20
    arm.hand(-20)
    time.sleep(1)
    # Control the elbow: -90 to 90
    arm.elbow(-90)
    time.sleep(1)
    # Control the shoulder: -90 to 90
    arm.shoulder(-90)
    time.sleep(1)
    # Control the base: -45 to 90
    arm.base(-45)
    time.sleep(1)
    arm.base(0)
    time.sleep(1)


finally:
    time.sleep(1)
    # arm.shutdown()