from robot_sdk.motion.motors import Motors
from robot_sdk.feedback.leds import LEDs
from robot_sdk.arm.arm import Arm
from robot_sdk.vision.camera import SimpleCamera
import time

# Initialize the robot's components
motors = Motors()
arm = Arm()
led = LEDs()
cam = SimpleCamera()


# Define the speed of the robot
SPEED = 40


plot_order = {
    "first" : "green",
    "second": "nothing",
    "third" : "orange"
}

# Assuming same starting position of the robot.

def detect_plot_order():
    print("[INFO] Detecting plot order...")

    # Plot detection from here
    iterations = 10
    initial_detected_order = cam.get_plot_order(min_area=500, target_colors=["green", "orange", "gray"])
    
    order = initial_detected_order

    # Repeat the detection until we get a consistent order for a few iterations to ensure reliability
    while iterations > 0:
        order = cam.get_plot_order(min_area=500, target_colors=["green", "orange", "gray"])
        print("[DEBUG] Detected order: {}".format(order))

        if order == initial_detected_order:
            iterations -= 1
        else:
            iterations = 10
            initial_detected_order = order
    
    # Assign the final detected order to the plot_order dictionary
    plot_order["first"] = order[0]
    plot_order["second"] = order[1]
    plot_order["third"] = order[2]

    print("[INFO] Detected order \n- First: {}, Second: {}, Third: {}".format(plot_order["first"], plot_order["second"], plot_order["third"]))

def initialize_robot_arm():
    # Initial setup for the robot, if needed
    print("[INFO] Initializing robot components...")
    # For example, we could reset the arm position here
    arm.base(35)
    arm.shoulder(0)
    arm.hand(0)
    print("[INFO] Robot initialization complete.")


def perform_action(color):
    """Perform an action at the color position, like flashing the LEDs."""
    if color == "gray":
        
        print("[INFO] Performing action at gray plot")
        led.both("white")
        time.sleep(2)
        led.both("off")
        pass

    elif color == "green":
        print("[INFO] Performing action at green plot")
        led.both("green")
        motors.rotate_left(SPEED)
        time.sleep(2.1)
        motors.stop()
        time.sleep(0.5)
        # Assuming the green seeds are in front
        # Drop seeds at the plot
        arm.base(0)
        time.sleep(0.5)
        initialize_robot_arm()
        # Always return to drive forward
        motors.rotate_right(SPEED)
        time.sleep(1.8)
        motors.stop()

        led.off()

    elif color == "orange":
        print("[INFO] Performing action at orange plot")
        led.both("orange")
        time.sleep(0.5)
        led.off()
    else:
        print("[INFO] Skip this plot")

def main():

    initialize_robot_arm()

    # Initial LED indication for starting the mission
    led.both("blue")
    time.sleep(1)
    led.off()

    
    # Step 1: Move to the position for detection
    motors.rotate_left(SPEED)
    time.sleep(0.5)
    motors.stop()
    # exit()
    # Step 2: Detect the order of the plots
    detect_plot_order()    
    
    # Step 3: Move to first plot
    motors.forward(SPEED)
    time.sleep(0.5)
    motors.forward(SPEED)
    time.sleep(0.7)
    motors.rotate_right(SPEED)
    time.sleep(0.6)
    motors.forward(SPEED)
    time.sleep(0.5)
    motors.stop()
    time.sleep(0.3)
    
    perform_action(plot_order["first"])

    # # Step 4: Move to second plot
    motors.forward(SPEED)
    time.sleep(0.5)

    perform_action(plot_order["second"])

    # Step 5: Move to third plot
    motors.forward(SPEED)
    time.sleep(0.5)
    motors.stop()

    perform_action(plot_order["third"])

    # Step 6: Move out of map
    motors.backward(SPEED)
    led.both("red")
    time.sleep(2)
    motors .stop()

    


if __name__ == "__main__":

    main()

    # detect_plot_order()


    exit()
