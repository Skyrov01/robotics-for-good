import time
from robot_sdk.vision.camera import SimpleCamera
from robot_sdk.arm.arm import Arm

# Create the camera and choose a starting color
cam = SimpleCamera("yellow")

# -----------------------------------
# Create a custom HSV color preset
# HSV = [Hue, Saturation, Value]
# Hue range: 0–180
# -----------------------------------

cam.set_color_range(
    lower=[172, 140, 80],
    upper=[180, 255, 255]
)

arm = Arm()
arm.base(60)

while True:
    print(cam.get_plot_order())
    time.sleep(0.05)
