import time
from robot_sdk.vision.camera import SimpleCamera


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

# Optional: calibrate a color by holding it in the center box
# This will update the color range automatically
# cam.calibrate_color(roi_size=80, samples=1)

while True:
    # Change the color you want to track
    # cam.set_color("blue")

    # Show the camera view and detect objects
    # All vision + drawing is handled internally
    running = cam.get_frame_with_detection()

    if not running:
        break

    time.sleep(0.05)
