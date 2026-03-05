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

firstColor = None
secondColor = None
thirdColor = None

def driveToFirst():
   try:
    m.forward(45)
    time.sleep(1)
    
    m.rotate_left(45)
    time.sleep(1)
    m.forward(45)
    time.sleep(0.4)
    m.rotate_right(45)
    time.sleep(1.25)
    m.forward(45)
    time.sleep(0.4)
    m.rotate_left(45)
    time.sleep(1.3)
    m.stop()
     
def driveToSecond():
  try:
    time.sleep(1)
    m.rotate_right(45)
    m.forward(0.85)
    m.rotate_right(45)
    m.forward(20) 
    m.rotate_right(45)
    time.sleep(1.25)
    m.forward(45)
    time.sleep(0.9)
    m.rotate_left(45)
    time.sleep(1.48)
    m.stop()
  
def driveToThird():
  try:
    time.sleep(1)
    m.rotate_right(45)
    time.sleep(1.25)
    m.forward(45)
    time.sleep(0.95)
    m.rotate_left(45)
    time.sleep(1.48)
    m.stop()

def detectColor(color)
  for i in range(10):
    detected, position, _, _, _, _, _ = cam.get_color_position(color_name=color, min_area=800)
    if (detect == true && position == "center")
      firstColor = "orange"
  

while True:
    # print(cam.get_plot_order())
    detected, position, _, _, _, _, _ = cam.get_color_position(color_name=color, min_area=800)
    print(f"Detected {color}: {detected}, Position: {position}")
    time.sleep(0.1)
